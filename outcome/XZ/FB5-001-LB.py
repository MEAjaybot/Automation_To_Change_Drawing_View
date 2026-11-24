import cadquery as cq
from ocp_vscode import show
LENGTH = 181
WIDTH = 150
THICKNESS = 6

HOLE1_X = 25
HOLE1_Y = 66
CBORE1_MINOR_DIAMETER = 6
CBORE1_MAJOR_DIAMETER = 12
CBORE1_MAJOR_DEPTH = 4
HOLE2_X = 134
HOLE2_Y = 94
CBORE2_MINOR_DIAMETER = 6
CBORE2_MAJOR_DIAMETER = 12
CBORE2_MAJOR_DEPTH = 3

CHAMFER_SIZE = 6

part = (
    cq.Workplane("XZ")
    .rect(LENGTH, WIDTH, centered=False)
    .extrude(-THICKNESS)
)

part = (
    part
    .edges("|Y")
    .chamfer(CHAMFER_SIZE)
)

part = (
    part
    .faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints([(HOLE1_X, HOLE1_Y)])
    .cboreHole(
        CBORE1_MINOR_DIAMETER,
        CBORE1_MAJOR_DIAMETER,
        CBORE1_MAJOR_DEPTH
    )
)

part = (
    part
    .faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints([(HOLE2_X, HOLE2_Y)])
    .cboreHole(
        CBORE2_MINOR_DIAMETER,
        CBORE2_MAJOR_DIAMETER,
        CBORE2_MAJOR_DEPTH
    )
)

show(part)