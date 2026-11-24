import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from ocp_vscode import show,ignore_camera_warnings
from pathlib import Path
import re
import os
from ocp_vscode import show, ignore_camera_warnings
from process import process_file


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


print("Selected view:", MODEL_VIEW)
files = list(INPUT_DIR.rglob("*.py"))

files = list(INPUT_DIR.glob("*.py"))
print("Python files found:", len(files))
MAX_WORKERS = 5
def main():

    files = list(INPUT_DIR.rglob("*.py"))

    print(f"Total files: {len(files)}")
    print(f"Using {MAX_WORKERS} workers")

    if not files:
        print("No Python files found.")
        return

    # Parallel conversion
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(process_file, file_path): file_path
            for file_path in files
        }

        output_files = []

        for future in as_completed(futures):

            file_path = futures[future]

            try:
                output_path = future.result()
                output_files.append(output_path)

            except Exception as e:
                print(f"[ERROR] {file_path.name}: {e}")

    print("\nAll file conversions completed.")

    # ----------------------------------
    # Execute and display models
    # ----------------------------------

    ignore_camera_warnings()

    for output_path in sorted(output_files):

        try:
            namespace = {"__name__": "__main__"}

            code = output_path.read_text(encoding="utf-8")

            exec(
                compile(code, str(output_path), "exec"),
                namespace
            )

            part = namespace["part"]

            show(part, reset_camera=True)

            print(f"Displayed: {output_path.name}")

        except Exception as e:
            print(f"[DISPLAY ERROR] {output_path.name}: {e}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()