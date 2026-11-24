import cadquery as cq
from ocp_vscode import show
LENGTH = 176
WIDTH = 83
THICKNESS = 18

CUTOUT1_X = 115
CUTOUT1_Y = 36
CUTOUT_LENGTH = 40
CUTOUT_WIDTH = 20
CUTOUT_LOCATIONS = [
    (CUTOUT1_X, CUTOUT1_Y),
]

part = (
    cq.Workplane("XZ")
    .rect(LENGTH, WIDTH, centered=False)
    .extrude(-THICKNESS)
)

part = (
    part
    .faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(CUTOUT_LOCATIONS)
    .rect(
        CUTOUT_LENGTH,
        CUTOUT_WIDTH
    )
    .cutThruAll()
)

show(part)