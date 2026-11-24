import cadquery as cq
from ocp_vscode import show
LENGTH = 157
WIDTH = 115
THICKNESS = 11

SLOT_LENGTH_C2C = 10
SLOT_WIDTH = 8

SLOT_DEPTH = 5

SLOT1_X = 50
SLOT1_Y = 37

SLOT1_ANGLE = 45
SLOT1_LOCATIONS = [
    (SLOT1_X, SLOT1_Y)
]

SLOT2_X = 111
SLOT2_Y = 37

SLOT2_ANGLE = 45
SLOT2_LOCATIONS = [
    (SLOT2_X, SLOT2_Y)
]

FILLET_EDGE_SELECTOR = "|Y"
FILLET_RADIUS = 4

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
    .edges(FILLET_EDGE_SELECTOR)
    .fillet(FILLET_RADIUS)
)

show(part)