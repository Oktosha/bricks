import argparse
import tomllib
import sys
import math
from dataclasses import dataclass
import random
import geom

EPS = 1e-8


@dataclass
class BrickWithFallenTeethData:
    type: str
    n_left_teeth: int
    n_right_teeth: int


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


def seq_len(seq: list[BrickWithFallenTeethData], config: dict) -> float:
    length = 0
    for brick in seq:
        length += config["bricks"][brick.type]["length"]
    if len(seq) > 1:
        length += config["joints"]["head"] * (len(seq) - 1)
    return length


def eq(a: float, b: float) -> bool:
    return abs(a - b) < EPS


def gen_full_brick_option(
    ptrn: list[list[BrickWithFallenTeethData]],
    course: int,
    config: dict,
    *,
    f_len: float,
    h_len: float,
    d_len: float,
    h_joint: float,
) -> list[BrickWithFallenTeethData]:
    q_len = config["bricks"]["q"]["length"]
    if course == 0:
        return BrickWithFallenTeethData("f", 1, 1)
    data = BrickWithFallenTeethData("f", 1, 1)
    x_left = seq_len(ptrn[course], config) + h_joint
    x_right = x_left + f_len
    for i in range(len(ptrn[course - 1])):
        e_left = seq_len(ptrn[course - 1][:i], config) + h_joint
        e_right = e_left + config["bricks"][ptrn[course - 1][i].type]["length"]
        if eq(e_right + h_joint - x_right, -q_len):
            data.n_left_teeth = ptrn[course - 1][i].n_left_teeth + 1
        if eq(e_right - x_right - h_joint, q_len):
            data.n_right_teeth = ptrn[course - 1][i].n_right_teeth + 1
    if data.n_left_teeth > 5 or data.n_right_teeth > 5:
        print("can't lay f due to teeth")
        return None
    return data


def gen_half_brick_option(
    ptrn: list[list[BrickWithFallenTeethData]],
    course: int,
    config: dict,
    *,
    f_len: float,
    h_len: float,
    d_len: float,
    h_joint: float,
) -> list[BrickWithFallenTeethData]:
    q_len = config["bricks"]["q"]["length"]
    if len(ptrn[course]) >= 1 and ptrn[course][-1].type == "h":
        print("prev brick is h")
        return None
    if course == 0:
        return BrickWithFallenTeethData("h", 1, 1)
    data = BrickWithFallenTeethData("h", 1, 1)
    x_left = seq_len(ptrn[course], config) + h_joint
    x_right = x_left + h_len
    for i in range(len(ptrn[course - 1])):
        e_left = seq_len(ptrn[course - 1][:i], config) + h_joint
        e_right = e_left + config["bricks"][ptrn[course - 1][i].type]["length"]
        if eq(e_right + h_joint - x_right, -q_len):
            data.n_left_teeth = ptrn[course - 1][i].n_left_teeth + 1
        if eq(e_right - x_right - h_joint, q_len):
            data.n_right_teeth = ptrn[course - 1][i].n_right_teeth + 1
        if e_left <= x_right and e_right >= x_left and ptrn[course - 1][i].type == "h":
            return None
    if data.n_left_teeth > 5 or data.n_right_teeth > 5:
        print("can't lay h due to teeth")
        return None
    return data


def gen_wild_options(
    ptrn: list[list[BrickWithFallenTeethData]],
    course: int,
    config: dict,
    *,
    f_len: float,
    h_len: float,
    d_len: float,
    h_joint: float,
) -> list[BrickWithFallenTeethData]:
    options = []
    full_brick_option = gen_full_brick_option(
        ptrn, course, config, f_len=f_len, h_len=h_len, d_len=d_len, h_joint=h_joint
    )
    if full_brick_option:
        options.append(full_brick_option)
    half_brick_option = gen_half_brick_option(
        ptrn, course, config, f_len=f_len, h_len=h_len, d_len=d_len, h_joint=h_joint
    )
    if half_brick_option:
        options.append(half_brick_option)
    return options


def get_wild_bond_pattern(config: dict) -> list[list[str]]:
    wall_w: float = config["wall"]["width"]
    wall_h: float = config["wall"]["height"]
    h_joint: float = config["joints"]["head"]
    bed_joint: float = config["joints"]["bed"]
    brick_height: float = config["bricks"]["f"]["height"]
    f_len: float = config["bricks"]["f"]["length"]
    h_len: float = config["bricks"]["h"]["length"]
    d_len: float = config["bricks"]["d"]["length"]
    course_height = bed_joint + brick_height
    n_courses = int(wall_h / course_height)
    if wall_h - course_height * n_courses > EPS:
        print(
            f"Error: The wall height {wall_h} can't be represented as a whole number of courses of height {course_height}",
            file=sys.stderr,
        )
        return None
    course = 0
    ptrn: list[list[BrickWithFallenTeethData]] = [[] for _ in range(n_courses)]
    n_full_course_retries = 0
    while course < n_courses:
        print(f"gen course {course}")
        if n_full_course_retries >= 100:
            print(
                "Retried full courses 100 times, now at course {course}, giving up",
                file=sys.stderr,
            )
            return None
        if course % 2 == 0:
            finish_len = h_joint + d_len + h_joint + h_len
            n_retries = 0
            should_regenerate_full_rows = False
            while wall_w - seq_len(ptrn[course], config) - finish_len > EPS:
                options = gen_wild_options(
                    ptrn,
                    course,
                    config,
                    f_len=f_len,
                    h_len=h_len,
                    d_len=d_len,
                    h_joint=h_joint,
                )
                if len(options) == 0:
                    # we regenerate 5 last bricks or all bricks in this course if there were less
                    if len(ptrn[course]) <= 5:
                        ptrn[course] = []
                    else:
                        ptrn[course] = ptrn[course][:-4]
                    n_retries += 1
                    continue
                if n_retries >= 10:
                    should_regenerate_full_rows = True
                    break
                ptrn[course].append(random.choice(options))

            if should_regenerate_full_rows:
                n_full_course_retries += 1
                ptrn[course] = []
                if course > 0:
                    ptrn[course - 1] = []
                    course = course - 1
                    continue
                else:
                    print(
                        f"Failed to generate course 0 according to the constrains",
                        file=sys.stderr,
                    )
                    return None

            finish_with_hd_len = h_joint + h_len + h_joint + d_len
            finish_with_d_len = h_joint + d_len
            if abs(wall_w - seq_len(ptrn[course], config) - finish_with_hd_len) < EPS:
                if ptrn[course][-1].type == "h":
                    ptrn[course].pop()
                    ptrn[course].extend(
                        [
                            BrickWithFallenTeethData("f", 1, 1),
                            BrickWithFallenTeethData("d", 1, 1),
                        ]
                    )
                else:
                    ptrn[course].extend(
                        [
                            BrickWithFallenTeethData("h", 1, 1),
                            BrickWithFallenTeethData("d", 1, 1),
                        ]
                    )
            elif abs(wall_w - seq_len(ptrn[course], config) - finish_with_d_len) < EPS:
                ptrn[course].append(BrickWithFallenTeethData("d", 1, 1))
            else:
                print(
                    f"Error: can't finish remaining {wall_w - seq_len(ptrn[course])} width of course {course} of wild bond",
                    file=sys.stderr,
                )
                return None
            course += 1
        elif course % 2 == 1:
            ptrn[course].append(BrickWithFallenTeethData("d", 1, 1))
            n_retries = 0
            should_regenerate_full_rows = False
            while wall_w - seq_len(ptrn[course], config) - (h_joint + f_len) > EPS:
                options = gen_wild_options(
                    ptrn,
                    course,
                    config,
                    f_len=f_len,
                    h_len=h_len,
                    d_len=d_len,
                    h_joint=h_joint,
                )
                if len(options) == 0:
                    # we regenerate 5 last bricks but we keep the first driklezoor brick
                    if len(ptrn[course]) <= 5:
                        ptrn[course] = ptrn[course][:1]
                    else:
                        ptrn[course] = ptrn[course][:-4]
                    n_retries += 1
                    continue
                if n_retries >= 10:
                    should_regenerate_full_rows = True
                    break
                ptrn[course].append(random.choice(options))
            if should_regenerate_full_rows:
                n_full_course_retries += 1
                ptrn[course] = []
                ptrn[course - 1] = []
                course = course - 1
                continue
            if abs(wall_w - seq_len(ptrn[course], config) - (h_joint + f_len)) < EPS:
                ptrn[course].append(BrickWithFallenTeethData("f", 1, 1))
            elif abs(wall_w - seq_len(ptrn[course], config) - (h_joint + h_len)) < EPS:
                ptrn[course].append(BrickWithFallenTeethData("h", 1, 1))
            else:
                print(
                    f"Error: can't finish remaining {wall_w - seq_len(ptrn[course])} width of course {course} of wild bond",
                    file=sys.stderr,
                )
                return None
            course += 1
    return [[x.type for x in c] for c in ptrn]


def get_pattern(config: dict):
    bond = config.get("bond", None)
    if bond == "stretcher":
        return get_stretcher_bond_pattern(config)
    elif bond == "english cross":
        return get_english_cross_bond_pattern(config)
    elif bond == "flemish":
        return get_flemish_bond_pattern(config)
    elif bond == "wild":
        return get_wild_bond_pattern(config)
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
