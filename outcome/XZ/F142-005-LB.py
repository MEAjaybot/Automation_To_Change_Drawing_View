import math
import cadquery as cq

LENGTH = 187
WIDTH = 121
THICKNESS = 27

part = (
    cq.Workplane("XZ")
    .rect(LENGTH, WIDTH, centered=False)
    .extrude(-THICKNESS)
)

HOLE1_X = 26
HOLE1_Y = 60.5
HOLE1_DIAMETER = 6.6
HOLE1_DEPTH = 13
HOLE1_DRILL_ANGLE = 118

HOLE2_X = 52
HOLE2_Y = 60.5
HOLE2_DIAMETER = 9
HOLE2_DEPTH = 16
HOLE2_DRILL_ANGLE = 118

HOLE3_X = 107
HOLE3_Y = 60.5
HOLE3_DIAMETER = 11
HOLE3_DEPTH = 20
HOLE3_DRILL_ANGLE = 118

HOLE_DATA = [
    (HOLE1_X, HOLE1_Y, HOLE1_DIAMETER, HOLE1_DEPTH, HOLE1_DRILL_ANGLE),
    (HOLE2_X, HOLE2_Y, HOLE2_DIAMETER, HOLE2_DEPTH, HOLE2_DRILL_ANGLE),
    (HOLE3_X, HOLE3_Y, HOLE3_DIAMETER, HOLE3_DEPTH, HOLE3_DRILL_ANGLE),
]

OVER = 1.0

for x, z, dia, depth, angle in HOLE_DATA:
    r = dia / 2.0
    plen = r / math.tan(math.radians(angle / 2.0))

    hole_tool = (
        cq.Workplane("XY")
        .polyline([
            (0, -OVER),
            (r, -OVER),
            (r, depth - plen),
            (0, depth),
        ])
        .close()
        .revolve(360, (0, 0), (0, 1))
        .translate((x, 0, z))
    )
    part = part.cut(hole_tool)

