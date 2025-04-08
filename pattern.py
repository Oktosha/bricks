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


def get_english_cross_bond_even_course(
    wall_width, full_brick_length, half_brick_length, quater_brick_length, head_joint
):
    if wall_width < full_brick_length:
        print(
            f"Error: can't generate odd course for english cross bond because wall width {wall_width} is smaller than full brick length {full_brick_length}",
            file=sys.stderr,
        )
        return None
    pattern = ["f"]
    l = wall_width - full_brick_length
    n = int(l / (full_brick_length + head_joint))
    pattern.extend(["f" for i in range(n)])
    r = l - n * (full_brick_length + head_joint)
    if r > EPS:
        print(
            f"Error: can't generate odd coursr for english cross bond because wall width {wall_width} doesn't whole number of full bricks of length {full_brick_length} with joints of {head_joint}",
            file=sys.stderr,
        )
        return None
    return pattern


def get_english_cross_bond_odd_course(
    wall_width, full_brick_length, half_brick_length, quater_brick_length, head_joint
):
    if (
        wall_width
        < quater_brick_length
        + head_joint
        + half_brick_length
        + head_joint
        + quater_brick_length
    ):
        print(
            f"Error: can't generate odd course for english cross bond because wall width {wall_width} is smaller than length of 2 quater bricks, 3 joins and a half brick",
            file=sys.stderr,
        )
        return None
    pattern = ["q"]
    l = wall_width - quater_brick_length
    n = int(l / (half_brick_length + head_joint))
    pattern.extend(["h" for i in range(n)])
    r = l - n * (half_brick_length + head_joint)
    if r > EPS:
        if math.fabs(head_joint + quater_brick_length - r) > EPS:
            print(
                f"Error: can't finish remaining {r} width of odd course of english cross bond with a quaterbrick of length {quater_brick_length} and joint of size {head_joint}",
                file=sys.stderr,
            )
            return None
        pattern.append("q")
    return pattern


def get_english_cross_bond_pattern(config: dict):
    wall_width = config["wall"]["width"]
    wall_height = config["wall"]["height"]
    head_joint = config["joints"]["head"]
    bed_joint = config["joints"]["bed"]
    brick_height = config["bricks"]["f"]["height"]
    full_brick_length = config["bricks"]["f"]["length"]
    half_brick_length = config["bricks"]["h"]["length"]
    quater_brick_length = config["bricks"]["q"]["length"]
    course_height = bed_joint + brick_height
    n_courses = int(wall_height / course_height)
    if wall_height - course_height * n_courses > EPS:
        print(
            f"Error: The wall height {wall_height} can't be represented as a whole number of courses of height {course_height}",
            file=sys.stderr,
        )
        return None
    even_course = get_english_cross_bond_even_course(
        wall_width,
        full_brick_length,
        half_brick_length,
        quater_brick_length,
        head_joint,
    )
    odd_course = get_english_cross_bond_odd_course(
        wall_width,
        full_brick_length,
        half_brick_length,
        quater_brick_length,
        head_joint,
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


def get_flemish_bond_even_course(
    wall_width, full_brick_length, half_brick_length, quater_brick_length, head_joint
):
    if (
        wall_width
        < quater_brick_length
        + full_brick_length
        + half_brick_length
        + half_brick_length
        + 3 * head_joint
    ):
        print(
            f"Error: can't generate odd course for Flemish bond because",
            f"wall width {wall_width} is smaller than full brick length {full_brick_length} plus",
            f"half brick lenght {half_brick_length} * 2 plus quater brick lenght {quater_brick_length} plus head joint {head_joint} * 3",
            file=sys.stderr,
            sep="\n",
        )
        return None
    pattern = ["q"]
    l = wall_width - quater_brick_length
    n = int(l / (head_joint + full_brick_length + head_joint + half_brick_length))
    for _ in range(n):
        pattern.extend(["f", "h"])
    r = l - n * (head_joint + full_brick_length + head_joint + half_brick_length)
    if r > EPS:
        if math.fabs(head_joint + half_brick_length - r) > EPS:
            print(
                f"Error: can't finish remaining {r} width of even course of Flemish bond with a half brick of length {half_brick_length} and joint of size {head_joint}",
                file=sys.stderr,
            )
            return None
        pattern.append("h")
    return pattern


def get_flemish_bond_odd_course(
    wall_width, full_brick_length, half_brick_length, quater_brick_length, head_joint
):
    if (
        wall_width
        < quater_brick_length
        + full_brick_length
        + half_brick_length
        + half_brick_length
        + 3 * head_joint
    ):
        print(
            f"Error: can't generate even course for Flemish bond because",
            f"wall width {wall_width} is smaller than full brick length {full_brick_length} plus",
            f"half brick lenght {half_brick_length} * 2 plus quater brick lenght {quater_brick_length} plus head joint {head_joint} * 3",
            file=sys.stderr,
            sep="\n",
        )
        return None
    pattern = ["h"]
    l = wall_width - half_brick_length
    n = int(l / (head_joint + half_brick_length + head_joint + full_brick_length))
    for _ in range(n):
        pattern.extend(["h", "f"])
    r = l - n * (head_joint + half_brick_length + head_joint + full_brick_length)
    if r > EPS:
        if math.fabs(head_joint + quater_brick_length - r) > EPS:
            print(
                f"Error: can't finish remaining {r} width of odd course of Flemish bond with a quater brick of length {quater_brick_length} and joint of size {head_joint}",
                file=sys.stderr,
            )
            return None
        pattern.append("q")
    return pattern


def get_flemish_bond_pattern(config: dict):
    wall_width = config["wall"]["width"]
    wall_height = config["wall"]["height"]
    head_joint = config["joints"]["head"]
    bed_joint = config["joints"]["bed"]
    brick_height = config["bricks"]["f"]["height"]
    full_brick_length = config["bricks"]["f"]["length"]
    half_brick_length = config["bricks"]["h"]["length"]
    quater_brick_length = config["bricks"]["q"]["length"]
    course_height = bed_joint + brick_height
    n_courses = int(wall_height / course_height)
    if wall_height - course_height * n_courses > EPS:
        print(
            f"Error: The wall height {wall_height} can't be represented as a whole number of courses of height {course_height}",
            file=sys.stderr,
        )
        return None
    even_course = get_flemish_bond_even_course(
        wall_width,
        full_brick_length,
        half_brick_length,
        quater_brick_length,
        head_joint,
    )
    odd_course = get_flemish_bond_odd_course(
        wall_width,
        full_brick_length,
        half_brick_length,
        quater_brick_length,
        head_joint,
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
    elif bond == "english cross":
        return get_english_cross_bond_pattern(config)
    elif bond == "flemish":
        return get_flemish_bond_pattern(config)
    else:
        print(f"bond {bond} unsupported", file=sys.stderr)
        return None


def print_pattern(pattern: list[list[str]]):
    for course in pattern:
        print(" ".join(course))


def load_from_file(file) -> list[list[str]]:
    pattern = []
    for line in file.readlines():
        pattern.append(line.strip().split())
    return pattern


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Pattern",
        description="Creates brick pattern for the given filename.wallconfig",
    )
    parser.add_argument("wallconfig")
    args = parser.parse_args()
    with open(args.wallconfig, "rb") as f:
        config = tomllib.load(f)
        pattern = get_pattern(config)
        if not (pattern is None):
            print_pattern(pattern)
