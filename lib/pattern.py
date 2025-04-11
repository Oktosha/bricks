import random
import sys

from dataclasses import dataclass


EPS = 1e-8


@dataclass
class BrickWithFallenTeethData:
    type: str
    n_left_teeth: int
    n_right_teeth: int


def eq(a: float, b: float) -> bool:
    return abs(a - b) < EPS


def get_total_n_bricks(ptrn: list[list[str]]):
    return sum(map(len, ptrn))


def get_stretcher_bond_even_course(
    wall_width, full_brick_length, half_brick_length, head_joint
):
    if wall_width < full_brick_length:
        print(
            f"Error: can't generate stretcher bond even course because wall width {wall_width} is smaller than full brick length {full_brick_length}",
            file=sys.stderr,
        )
        return None
    pattern = ["f"]
    l = wall_width - full_brick_length
    n = int(l / (full_brick_length + head_joint))
    pattern.extend(["f" for _ in range(n)])
    r = l - n * (full_brick_length + head_joint)
    if not eq(r, 0):
        if not eq(r, head_joint + half_brick_length):
            print(
                f"Error: can't finish remaining {r} width of stretcher bond with a halfbrick of length {half_brick_length} and a joint of size {head_joint}",
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
    if not eq(r, 0):
        if not eq(head_joint + half_brick_length, r):
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
    if not eq(wall_height, course_height * n_courses):
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
    if not eq(r, 0):
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
    if not eq(r, 0):
        if not eq(head_joint + quater_brick_length, r):
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
    if not eq(wall_height, course_height * n_courses):
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
    if not eq(r, 0):
        if not eq(head_joint + half_brick_length, r):
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
    if not eq(r, 0):
        if not eq(head_joint + quater_brick_length, r):
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


def gen_full_brick_option(
    ptrn: list[list[BrickWithFallenTeethData]], course: int, config: dict
) -> list[BrickWithFallenTeethData]:
    """
    This function returns BrickWithFallenTeethData for full brick if it's possible to lay such brick
    Or None if it if impossible to lay such brick according to the rules
    For now the only rule that can prevent full brick from laying is the fallen teeth rule
    """
    q_len = config["bricks"]["q"]["length"]
    f_len = config["bricks"]["f"]["length"]
    h_joint = config["joints"]["head"]
    if course == 0:
        return BrickWithFallenTeethData("f", 1, 1)
    data = BrickWithFallenTeethData("f", 1, 1)
    x_left = seq_len(ptrn[course], config) + h_joint
    x_right = x_left + f_len
    # Looking at all the bricks beneath the given brick to count the "fallen teeth" strikes
    # We add the fallen teeth strike from a break beneath if the difference between
    # the edge positions has the length of a quater brick (+- joint, depends on the side)
    for i in range(len(ptrn[course - 1])):
        beneath_type = ptrn[course - 1][i].type
        beneath_left = seq_len(ptrn[course - 1][:i], config) + h_joint
        beneath_right = beneath_left + config["bricks"][beneath_type]["length"]
        if eq(beneath_right + h_joint - x_right, -q_len):
            data.n_left_teeth = ptrn[course - 1][i].n_left_teeth + 1
        if eq(beneath_right - x_right - h_joint, q_len):
            data.n_right_teeth = ptrn[course - 1][i].n_right_teeth + 1
    if data.n_left_teeth > 5 or data.n_right_teeth > 5:
        return None
    return data


def gen_half_brick_option(
    ptrn: list[list[BrickWithFallenTeethData]], course: int, config: dict
) -> list[BrickWithFallenTeethData]:
    """
    This function returns BrickWithFallenTeethData for half brick if it's possible to lay such brick
    Or None if it if impossible to lay such brick according to the rules
    The rules that can prevent half brick from laying are
     1. the fallen teeth rule
     2. "no 2 half bricks next to each other" rule
    """
    q_len = config["bricks"]["q"]["length"]
    h_len = config["bricks"]["h"]["length"]
    h_joint = config["joints"]["head"]
    # checking if the previous brick (brick to the left) is a half brick
    if len(ptrn[course]) >= 1 and ptrn[course][-1].type == "h":
        return None
    if course == 0:
        return BrickWithFallenTeethData("h", 1, 1)
    data = BrickWithFallenTeethData("h", 1, 1)
    x_left = seq_len(ptrn[course], config) + h_joint
    x_right = x_left + h_len
    # Looking at all the bricks beneath the given brick to count the "fallen teeth" strikes
    # We add the fallen teeth strike from a break beneath if the difference between
    # the edge positions has the length of a quater brick (+- joint, depends on the side)
    # Also looking if the brick beneath is a half brick (also forbidden)
    for i in range(len(ptrn[course - 1])):
        beneath_type = ptrn[course - 1][i].type
        beneath_left = seq_len(ptrn[course - 1][:i], config) + h_joint
        beneath_right = beneath_left + config["bricks"][beneath_type]["length"]
        if eq(beneath_right + h_joint - x_right, -q_len):
            data.n_left_teeth = ptrn[course - 1][i].n_left_teeth + 1
        if eq(beneath_right - x_right - h_joint, q_len):
            data.n_right_teeth = ptrn[course - 1][i].n_right_teeth + 1
        if beneath_left <= x_right and beneath_right >= x_left and beneath_type == "h":
            return None
    if data.n_left_teeth > 5 or data.n_right_teeth > 5:
        return None
    return data


def gen_wild_options(
    ptrn: list[list[BrickWithFallenTeethData]], course: int, config: dict
) -> list[BrickWithFallenTeethData]:
    options = []
    full_brick_option = gen_full_brick_option(ptrn, course, config)
    if full_brick_option:
        options.append(full_brick_option)
    half_brick_option = gen_half_brick_option(ptrn, course, config)
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
    if not eq(wall_h, course_height * n_courses):
        print(
            f"Error: The wall height {wall_h} can't be represented as a whole number of courses of height {course_height}",
            file=sys.stderr,
        )
        return None
    course = 0
    ptrn: list[list[BrickWithFallenTeethData]] = [[] for _ in range(n_courses)]
    n_full_course_retries = 0
    while course < n_courses:
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
                options = gen_wild_options(ptrn, course, config)
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
            if eq(wall_w - seq_len(ptrn[course], config), finish_with_hd_len):
                if ptrn[course][-1].type == "h":
                    ptrn[course].pop()
                    ptrn[course].append(BrickWithFallenTeethData("f", 1, 1))
                    ptrn[course].append(BrickWithFallenTeethData("d", 1, 1))
                else:
                    ptrn[course].append(BrickWithFallenTeethData("h", 1, 1))
                    ptrn[course].append(BrickWithFallenTeethData("d", 1, 1))
            elif eq(wall_w - seq_len(ptrn[course], config), finish_with_d_len):
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
                options = gen_wild_options(ptrn, course, config)
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
            if eq(wall_w - seq_len(ptrn[course], config), h_joint + f_len):
                ptrn[course].append(BrickWithFallenTeethData("f", 1, 1))
            elif eq(wall_w - seq_len(ptrn[course], config), h_joint + h_len):
                ptrn[course].append(BrickWithFallenTeethData("h", 1, 1))
            else:
                print(
                    f"Error: can't finish remaining {wall_w - seq_len(ptrn[course])} width of course {course} of wild bond",
                    file=sys.stderr,
                )
                return None
            course += 1
    return [[x.type for x in c] for c in ptrn]


def get_pattern(config: dict) -> list[list[str]]:
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
