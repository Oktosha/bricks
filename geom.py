from typing import NamedTuple


class PositionInPattern(NamedTuple):
    x: int
    y: int


class Point(NamedTuple):
    x: float
    y: float


def bottom_left_coordinates_of_a_brick(
    brick: PositionInPattern, config: dict, pattern: list[list[str]]
) -> Point:
    y = brick.y * (
        config["bricks"][pattern[brick.y][brick.x]]["height"] + config["joints"]["bed"]
    )
    x = 0
    for x_pos in range(brick.x):
        x += (
            config["bricks"][pattern[brick.y][x_pos]]["length"]
            + config["joints"]["head"]
        )
    return Point(x, y)
