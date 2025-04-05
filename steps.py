import argparse
import tomllib
import pattern
from typing import NamedTuple
import sys

class PositionInPattern(NamedTuple):
    x: int
    y: int

class Point(NamedTuple):
    x: float
    y: float

class Stride(NamedTuple):
    envelope_pos: Point
    steps: list[PositionInPattern]

def generate_coordinates_for_all_bricks(pattern) -> set[PositionInPattern]:
    coordinates = set()
    for (y,course) in enumerate(pattern):
        for (x,_) in enumerate(course):
            coordinates.add(PositionInPattern(x, y))
    return coordinates

def bottom_left_coordinates_of_a_brick(brick: PositionInPattern, config: dict, pattern: list[list[str]]) -> Point:
    y = brick.y * (config["bricks"][pattern[brick.y][brick.x]]["height"] + config["joints"]["bed"])
    x = 0
    for x_pos in range(brick.x):
        x += config["bricks"][pattern[brick.y][x_pos]]["length"] + config["joints"]["head"]
    return Point(x, y)

def find_the_leftmost_of_the_bottomest_unlayed_bricks(remaining_bricks: set[PositionInPattern]):
    brick = next(iter(remaining_bricks))
    for e in remaining_bricks:
        if e.y < brick.y:
            brick = e
        elif e.y == brick.y and e.x < brick.x:
            brick = e
    return brick

def can_lay(brick: PositionInPattern, envelope_pos: Point, remaining_bricks: set[PositionInPattern], config: dict, pattern: list[list[str]]) -> bool:
    brick_bottom_left = bottom_left_coordinates_of_a_brick(brick, config, pattern)
    brick_length = config["bricks"][pattern[brick.y][brick.x]]["length"]
    brick_height = config["bricks"][pattern[brick.y][brick.x]]["height"]
    envelope_height = config["envelope"]["height"]
    envelope_width = config["envelope"]["width"]

    # Here I check that the brick is completely within the envelope
    # I'm not checking that the joints around this brick are whithin the envelope
    # TODO: check that the joints are within the envelope
    if brick_bottom_left.x < envelope_pos.x or brick_bottom_left.y < envelope_pos.y:
        return False
    if brick_bottom_left.x + brick_length > envelope_pos.x + envelope_width or brick_bottom_left.y + brick_height > envelope_pos.y + envelope_height:
        return False
    
    # Here I check that all the bricks right beneath the given brick are already layed
    if brick.y == 0:
        return True
    for e_x, e_type in enumerate(pattern[brick.y - 1]):
        e_pos = PositionInPattern(e_x, brick.y - 1)
        e_left = bottom_left_coordinates_of_a_brick(e_pos, config, pattern).x
        e_right = e_left + config["bricks"][e_type]["length"]
        is_right_beneath = e_left <= brick_bottom_left.x + brick_length and e_right >= brick_bottom_left.x
        if is_right_beneath and e_pos in remaining_bricks:
            return False
    return True


def get_instructions(config: dict, pattern: list[list[str]]) -> list[Stride]:
    remaining_bricks = generate_coordinates_for_all_bricks(pattern)
    instructions: list[Stride] = []
    while len(remaining_bricks) > 0:
        next_brick = find_the_leftmost_of_the_bottomest_unlayed_bricks(remaining_bricks)
        envelope_pos = bottom_left_coordinates_of_a_brick(next_brick, config, pattern)
        instructions.append(Stride(envelope_pos, [next_brick]))
        remaining_bricks.remove(next_brick)
        while True:
            next_brick = None
            for brick in remaining_bricks:
                if can_lay(brick, envelope_pos, remaining_bricks, config, pattern):
                    next_brick = brick
                    break
            if next_brick:
                remaining_bricks.remove(next_brick)
                instructions[-1].steps.append(next_brick)
            else:
                break
    return instructions

def print_instructions(instructions: list[Stride]):
    for stride in instructions:
        print(f"move {stride.envelope_pos.x} {stride.envelope_pos.y}")
        for step in stride.steps:
            print(f"lay {step.x} {step.y}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Steps",
        description="Creates lay down steps for the given filename.wallconfig and filename.brickpattern",
    )
    parser.add_argument("wallconfig")
    parser.add_argument("brickpattern")
    args = parser.parse_args()
    with open(args.wallconfig, "rb") as configfile:
        with open(args.brickpattern, "r") as patternfile:
            config = tomllib.load(configfile)
            ptrn = pattern.load_from_file(patternfile)
            instructions = get_instructions(config, ptrn)
            print_instructions(instructions)