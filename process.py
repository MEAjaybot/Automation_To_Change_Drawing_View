
from pathlib import Path
import re
import os
from ocp_vscode import show, ignore_camera_warnings


BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"
print("Logical CPU cores:", os.cpu_count())
# Select view from environment variable
MODEL_VIEW = os.getenv("MODEL_VIEW", "XZ").upper()

# Define transformations for each view
VIEW_CONFIG = {
    "XZ": {
        "workplane": "XZ",
        "extrude_sign": "-",
        "edge_axis": "Y",
        "face_selector": "<Y",
        "groove_extrude_sign": "-",
        "groove_rotation_axis": "Y",
        "groove_angle_sign": "-",
        "groove_translation": "xz",
    },
    "YZ": {
        "workplane": "YZ",
        "extrude_sign": "+",
        "edge_axis": "X",
        "face_selector": ">X",
    },
}

if MODEL_VIEW not in VIEW_CONFIG:
    raise ValueError(
        f"Invalid MODEL_VIEW: {MODEL_VIEW}. Choose XZ or YZ."
    )

config = VIEW_CONFIG[MODEL_VIEW]

# Separate output folder for each view
OUTPUT_DIR = BASE_DIR / "outcome" / MODEL_VIEW
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)




def process_file(file_path):

    print(f"[Worker] Processing: {file_path.name}")

    # Preserve folder structure if input has subfolders
    output_path = OUTPUT_DIR / file_path.relative_to(INPUT_DIR)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip if output already exists
    if output_path.exists():
        print("Skipped:", file_path.name)
        return output_path

    code = file_path.read_text(encoding="utf-8")
    # Swap WIDTH and THICKNESS if THICKNESS > WIDTH for F129
    match = re.search(
        r'WIDTH\s*=\s*(\d+)\s*\n\s*THICKNESS\s*=\s*(\d+)',
        code
    )

    if match:
        width = int(match.group(1))
        thickness = int(match.group(2))

        if thickness > width:
            code = re.sub(
                r'WIDTH\s*=\s*\d+',
                f'WIDTH = {thickness}',
                code,
                count=1
            )

            code = re.sub(
                r'THICKNESS\s*=\s*\d+',
                f'THICKNESS = {width}',
                code,
                count=1
            )

    # 1. Change original XY workplane to selected plane
    code = re.sub(
        r'\.Workplane\(\s*["\']XY["\']\s*\)',
        f'.Workplane("{config["workplane"]}")',
        code
    )

    # 2. Change extrusion direction
    code = re.sub(
        r'\.extrude\(\s*THICKNESS\s*\)',
        f'.extrude({config["extrude_sign"]}THICKNESS)',
        code
    )

    # 3. Change edge selector
    code = re.sub(
        r'\.edges\(\s*["\']\|Z["\']\s*\)',
        f'.edges("|Y")',
        code
    )

    # 4. Change fillet edge selector
    code = re.sub(
        r'(FILLET_EDGE_SELECTOR\s*=\s*)["\']\|Z["\']',
        rf'\1"|{config["edge_axis"]}"',
        code
    )

    # 5. Change face selector
    code = re.sub(
        r'\.faces\(\s*["\']>Z["\']\s*\)',
        f'.faces("{config["face_selector"]}")',
        code
    )
    # 6. Change groove workplane XY -> XZ
    code = re.sub(
        r'cq\.Workplane\(\s*["\']XY["\']\s*\)',
        f'cq.Workplane("{config["workplane"]}")',
        code
    )

    # 7. Change groove extrusion direction
    code = re.sub(
        r'\.extrude\(\s*GROOVE_DEPTH\s*\)',
        f'.extrude({config["groove_extrude_sign"]}GROOVE_DEPTH)',
        code
    )

    # 8. Change groove rotation axis
    code = re.sub(
        r'\.rotate\(\s*\(0,\s*0,\s*0\),\s*\(0,\s*0,\s*1\),\s*GROOVE_ANGLE\s*\)',
        f'.rotate((0, 0, 0), (0, 1, 0), -GROOVE_ANGLE)',
        code
    )

    # 9. Change groove translation XY -> XZ
    code = re.sub(
        r'\.translate\(\s*\(x,\s*y,\s*THICKNESS\s*-\s*GROOVE_DEPTH\)\s*\)',
        '.translate((x, 0, y))',
        code
    )
    #  10. change Corner Cut XY -> XZ
    code = re.sub(r"\.NeraestToPointSelector\(\s*\(\s*0,\s*WIDTH,\s*0\s*\)\s*\)", ".NearestToPointSelector((0, 0, WIDTH))", code)


    # 11. Swap hole coordinates: (U, V) -> (V, U)
    code = re.sub(
        r'\(HOLE(\d+)_U,\s*HOLE(\d+)_V\)',
        lambda m: f'(HOLE{m.group(2)}_V, HOLE{m.group(1)}_U)',
        code
    )
    # Swap HOLE_LOCATIONS coordinates only for workplanes with explicit origin
    # Swap HOLE_LOCATIONS only when workplane has explicit origin=(0, 0, 0)

    pattern = (
        r'\.workplane\(\s*centerOption\s*=\s*["\']ProjectedOrigin["\']'
        r'\s*,\s*origin\s*=\s*\(\s*0\s*,\s*0\s*,\s*0\s*\)\s*\)'
        r'.*?\.pushPoints\(HOLE_LOCATIONS\)'
    )

    if re.search(pattern, code, flags=re.DOTALL):

        code = re.sub(
            r'\(HOLE(\d+)_X\s*,\s*HOLE(\d+)_Y\)',
            lambda m: f'(HOLE{m.group(1)}_Y, HOLE{m.group(2)}_X)',
            code
        )
    
    # 13# Convert center_hole from XY to XZ For F91-001-LB.py
    code = re.sub(
        r'(center_hole\s*=\s*\(\s*cq\.Workplane\()\s*["\']XY["\']\s*,\s*origin\s*=\s*\(0,\s*0,\s*THICKNESS\)\s*\)',
        r'\1"XZ", origin=(0, 0, THICKNESS))',
        code
    )
    # 14 # Convert flat_edge_holes from XY to XZ
    code = re.sub(
        r'(flat_edge_holes\s*=\s*\(\s*cq\.Workplane\()\s*["\']XY["\']\s*,\s*origin\s*=\s*\(0,\s*0,\s*THICKNESS\)\s*\)',
        r'\1"XZ", origin=(0, 0, THICKNESS))',
        code
    )
    #15 Convert boss workplane from XY to XZ
    code = re.sub(
        r'(boss\s*=\s*\(\s*cq\.Workplane\()\s*["\']XY["\']\s*,\s*origin\s*=\s*\(0,\s*0,\s*THICKNESS\)\s*\)',
        r'\1"XZ", origin=(0, 0, THICKNESS))',
        code
    )
    # 16 Convert chamfer edge selector from |Z to |Y
    
    code = re.sub(
        r'(CHAMFER_EDGE_SELECTOR\s*=\s*)["\']\|Z["\']',
        r'\1"|Y"',
        code
    )
    #17 Convert NearestToPointSelector point from XY to XZ
    code = re.sub(
        r'NearestToPointSelector\(\s*\(\s*0\s*,\s*WIDTH\s*,\s*0\s*\)\s*\)',
        'NearestToPointSelector((0, 0, WIDTH))',
        code
    )
    pattern = re.compile(
        r'(?ms)^(?P<indent>[ \t]*)top_z\s*=.*\r?\n'
        r'[ \t]*for\s+x,\s*y,\s*dia,\s*depth,\s*angle\s+in\s+HOLE_DATA\s*:\s*\r?\n'
        r'.*?^[ \t]*part\s*=\s*part\.cut\(hole_tool\)[ \t]*(?:#.*)?$'
    )

    def replace_drill(match):
        i = match.group("indent")
        j = i + "    "

        lines = [
            "OVER = 1.0",
            "",
            f"{i}for x, z, dia, depth, angle in HOLE_DATA:",
            f"{j}r = dia / 2.0",
            f"{j}plen = r / math.tan(math.radians(angle / 2.0))",
            "",
            f"{j}hole_tool = (",
            f'{j}    cq.Workplane("XY")',
            f"{j}    .polyline([",
            f"{j}        (0, -OVER),",
            f"{j}        (r, -OVER),",
            f"{j}        (r, depth - plen),",
            f"{j}        (0, depth),",
            f"{j}    ])",
            f"{j}    .close()",
            f"{j}    .revolve(360, (0, 0), (0, 1))",
            f"{j}    .translate((x, 0, z))",
            f"{j})",
            f"{j}part = part.cut(hole_tool)",
        ]

        return "\n".join(i + line if line else "" for line in lines)

    code, count = re.subn(pattern, replace_drill, code, count=1)

    if count:
        print("Successfully converted drill-hole pattern")
    else:
        print("Drill-hole pattern not found:", file_path.name)
    output_path.write_text(code, encoding="utf-8")

    print(f"[Worker] Completed: {output_path.name}")

    return output_path

    """print("Saved:", output_path)
    namespace = {}

    exec(compile(code, str(output_path), "exec"), namespace)

    # Retrieve generated 3D model
    part = namespace["part"]

    # Display in OCP CAD Viewer
    show(part, reset_camera=True)
    ignore_camera_warnings()"""


