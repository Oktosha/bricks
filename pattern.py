import argparse
import tomllib
import sys
import math

EPS = 1e-8

def get_stretcher_bond_even_course(
    wall_width, full_brick_length, half_brick_length, head_joint
):
    if wall_width < full_brick_length:
        print(
            f"Error: can't generate even course because wall width {wall_width} is smaller than full brick length {full_brick_length}",
            file=sys.stderr,
        )
        return None
    pattern = ["f"]
    l = wall_width - full_brick_length
    n = int(l / (full_brick_length + head_joint))
    pattern.extend(["f" for i in range(n)])
    r = l - n * (full_brick_length + head_joint)
    if r > EPS:
        if math.fabs(head_joint + half_brick_length - r) > EPS:
            print(
                f"Error: can't finish remaining {r} width with a halfbrick of length {half_brick_length} and joint of size {head_joint}",
                file=sys.stderr,
            )
            return None
        pattern.append("h")
    return pattern


def get_stretcher_bond_odd_course(
    wall_width, full_brick_length, half_brick_length, head_joint
):
    if wall_width < half_brick_length:
        print(
            f"Error: can't generate odd course because wall width {wall_width} is smaller than half brick length {half_brick_length}",
            file=sys.stderr,
        )
        return None
    pattern = ["h"]
    l = wall_width - half_brick_length
    n = int(l / (full_brick_length + head_joint))
    pattern.extend(["f" for i in range(n)])
    r = l - n * (full_brick_length + head_joint)
    if r > EPS:
        if math.fabs(head_joint + half_brick_length - r) > EPS:
            print(
                f"Error: can't finish remaining {r} width with a halfbrick of length {half_brick_length} and joint of size {head_joint}",
                file=sys.stderr,
            )
            return None
        pattern.append("h")
    return pattern


def get_stretcher_bond_pattern(config: dict):
    wall_width = config["wall"]["width"]
    wall_height = config["wall"]["height"]
    head_joint = config["joints"]["head"]
    bed_joint = config["joints"]["bed"]
    brick_height = config["bricks"]["f"]["height"]
    full_brick_length = config["bricks"]["f"]["length"]
    half_brick_length = config["bricks"]["h"]["length"]
    course_height = bed_joint + brick_height
    n_courses = int(wall_height / course_height)
    if wall_height - course_height * n_courses > EPS:
        print(
            f"Error: The wall height {wall_height} can't be represented as a whole number of courses of height {course_height}",
            file=sys.stderr,
        )
        return None
    even_course = get_stretcher_bond_even_course(
        wall_width, full_brick_length, half_brick_length, head_joint
    )
    odd_course = get_stretcher_bond_odd_course(
        wall_width, full_brick_length, half_brick_length, head_joint
    )
    if even_course is None or odd_course is None:
        return None
    pattern = []
    for i in range(n_courses):
        if i % 2 == 0:
            pattern.append([e for e in even_course])
        else:
            pattern.append([e for e in odd_course])
    return pattern


def get_pattern(config: dict):
    bond = config.get("bond", None)
    if bond == "stretcher":
        return get_stretcher_bond_pattern(config)
    else:
        print(f"bond {bond} unsupported", file=sys.stderr)
        return None


def print_pattern(pattern: list[list[str]]):
    for course in pattern:
        print(" ".join(course))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Pattern",
        description="Creates brick pattern for the given filename.wallconfig",
    )
    parser.add_argument("filename")
    args = parser.parse_args()
    with open(args.filename, "rb") as f:
        config = tomllib.load(f)
        pattern = get_pattern(config)
        if not (pattern is None):
            print_pattern(pattern)
