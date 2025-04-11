from typing import NamedTuple


class PositionInPattern(NamedTuple):
    x: int
    y: int


class Point(NamedTuple):
    x: float
    y: float


def brick_bottom_left(
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


class Stride(NamedTuple):
    envelope_pos: Point
    steps: list[PositionInPattern]


def generate_positions_in_pattern_for_all_bricks(pattern) -> set[PositionInPattern]:
    positions = set()
    for y, course in enumerate(pattern):
        for x, _ in enumerate(course):
            positions.add(PositionInPattern(x, y))
    return positions


def find_the_leftmost_of_the_bottomest_unlayed_bricks(
    remaining_bricks: set[PositionInPattern],
):
    brick = next(iter(remaining_bricks))
    for e in remaining_bricks:
        if e.y < brick.y:
            brick = e
        elif e.y == brick.y and e.x < brick.x:
            brick = e
    return brick


def can_lay(
    brick: PositionInPattern,
    envelope_pos: Point,
    remaining_bricks: set[PositionInPattern],
    config: dict,
    pattern: list[list[str]],
) -> bool:
    brick_bottom_left_x, brick_bottom_left_y = brick_bottom_left(brick, config, pattern)
    brick_length = config["bricks"][pattern[brick.y][brick.x]]["length"]
    brick_height = config["bricks"][pattern[brick.y][brick.x]]["height"]
    envelope_height = config["envelope"]["height"]
    envelope_width = config["envelope"]["width"]

    # Here I check that the brick is completely within the envelope
    # I'm not checking that the joints around this brick are whithin the envelope
    # TODO: check that the joints are within the envelope
    if brick_bottom_left_x < envelope_pos.x or brick_bottom_left_y < envelope_pos.y:
        return False
    if (
        brick_bottom_left_x + brick_length > envelope_pos.x + envelope_width
        or brick_bottom_left_y + brick_height > envelope_pos.y + envelope_height
    ):
        return False

    # Here I check that all the bricks right beneath the given brick are already layed
    if brick.y == 0:
        return True
    for e_x, e_type in enumerate(pattern[brick.y - 1]):
        e_pos = PositionInPattern(e_x, brick.y - 1)
        e_left = brick_bottom_left(e_pos, config, pattern).x
        e_right = e_left + config["bricks"][e_type]["length"]
        is_right_beneath = (
            e_left <= brick_bottom_left_x + brick_length
            and e_right >= brick_bottom_left_x
        )
        if is_right_beneath and e_pos in remaining_bricks:
            return False
    return True


# returns the list of layed bricks
def lay_bricks_at_envelope_pos(
    envelope_pos: Point,
    remaining_bricks: set[PositionInPattern],
    config: dict,
    pattern: list[list[str]],
) -> list[PositionInPattern]:
    remaining_bricks = remaining_bricks.copy()  # I don't want to alter remaining bricks
    layed_bricks = []
    while True:
        next_brick = None
        for brick in remaining_bricks:
            if can_lay(brick, envelope_pos, remaining_bricks, config, pattern):
                next_brick = brick
                break
        if next_brick:
            remaining_bricks.remove(next_brick)
            layed_bricks.append(next_brick)
        else:
            break
    return layed_bricks


def find_best_next_envelope_pos(
    remaining_bricks: set[PositionInPattern], config: dict, pattern: list[list[str]]
):
    bottom_brick_pos = find_the_leftmost_of_the_bottomest_unlayed_bricks(
        remaining_bricks
    )
    bottom_brick_coord = brick_bottom_left(bottom_brick_pos, config, pattern)
    best_n_layed_bricks = 0
    best_envelope_pos = Point(0, 0)
    for i in range(min(3, len(pattern) - bottom_brick_pos.y)):
        for x_pos in range(len(pattern[bottom_brick_pos.y + i])):
            brick_pos = PositionInPattern(x_pos, bottom_brick_pos.y + i)
            brick_coord = brick_bottom_left(brick_pos, config, pattern)
            envelope_pos = Point(brick_coord.x, bottom_brick_coord.y)
            n_layed_bricks = len(
                lay_bricks_at_envelope_pos(
                    envelope_pos, remaining_bricks, config, pattern
                )
            )
            if n_layed_bricks > best_n_layed_bricks:
                best_n_layed_bricks = n_layed_bricks
                best_envelope_pos = envelope_pos
    return best_envelope_pos


def get_instructions(config: dict, pattern: list[list[str]]) -> list[Stride]:
    remaining_bricks = generate_positions_in_pattern_for_all_bricks(pattern)
    instructions: list[Stride] = []
    while len(remaining_bricks) > 0:
        envelope_pos = find_best_next_envelope_pos(remaining_bricks, config, pattern)
        layed_bricks = lay_bricks_at_envelope_pos(
            envelope_pos, remaining_bricks, config, pattern
        )
        instructions.append(Stride(envelope_pos, layed_bricks))
        remaining_bricks.difference_update(layed_bricks)
    return instructions


def print_instructions(instructions: list[Stride]):
    for stride in instructions:
        print(f"move {stride.envelope_pos.x} {stride.envelope_pos.y}")
        for step in stride.steps:
            print(f"lay {step.x} {step.y}")
