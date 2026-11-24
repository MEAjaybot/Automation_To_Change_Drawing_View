import cadquery as cq

LENGTH = 128
WIDTH = 86
THICKNESS = 38

SLOT_LENGTH_C2C = 16
SLOT_WIDTH = 8

SLOT_DEPTH = 11

SLOT1_X = 30
SLOT1_Y = 27

SLOT1_ANGLE = 0
SLOT1_LOCATIONS = [
    (SLOT1_X, SLOT1_Y)
]

SLOT2_X = 65
SLOT2_Y = 27

SLOT2_ANGLE = 0
SLOT2_LOCATIONS = [
    (SLOT2_X, SLOT2_Y)
]

CHAMFER_EDGE_SELECTOR = "|Y"
CHAMFER_SIZE = 4

part = (
    cq.Workplane("XZ")
    .rect(LENGTH, WIDTH, centered=False)
    .extrude(-THICKNESS)
)

part = (
    part
    .faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(SLOT1_LOCATIONS)
    .slot2D(SLOT_LENGTH_C2C + SLOT_WIDTH, SLOT_WIDTH, SLOT1_ANGLE)
    .cutBlind(-SLOT_DEPTH)
)
part = (
    part
    .faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(SLOT2_LOCATIONS)
    .slot2D(SLOT_LENGTH_C2C + SLOT_WIDTH, SLOT_WIDTH, SLOT2_ANGLE)
    .cutBlind(-SLOT_DEPTH)
)
part = (
    part
    .edges(CHAMFER_EDGE_SELECTOR)
    .chamfer(CHAMFER_SIZE)
)

