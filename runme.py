import argparse
import sys
import tomllib

from lib import pattern, steps


def get_config(filename: str) -> dict:
    print(f"Loading wallconfig from {filename}", file=sys.stderr)
    file = open(filename, "rb")
    return tomllib.load(file)


def get_pattern(filename: str | None, config: dict) -> list[list[str]]:
    if filename:
        print(f"Loading brickpattern from {filename}", file=sys.stderr)
        file = open(filename, "r")
        return pattern.load_from_file(file)
    print(f"Generating brickpattern...", file=sys.stderr)
    return pattern.get_pattern(config)


def get_instructions(
    filename: str | None, config: dict, ptrn: list[list[str]]
) -> list[steps.Stride]:
    if filename:
        print(f"Loading bricksteps from {filename}", file=sys.stderr)
        file = open(filename, "r")
        return steps.load_from_file(file)
    print(f"Generating steps...", file=sys.stderr)
    return steps.get_instructions(config, ptrn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Brick Laying Viz",
        description="Visualizes laying down different bonds of bricks",
    )
    parser.add_argument(
        "--wallconfig",
        help="Configuration of the wall, see the example .wallconfig files",
        default="stretcher_bond.wallconfig",
    )
    parser.add_argument(
        "--brickpattern",
        help="Pregenerated wall pattern, useful when you want the same random wild bond wall",
    )
    parser.add_argument(
        "--bricksteps",
        help="Pregenerated laying steps, useful when you don't want to wait for the generation again",
    )
    parser.add_argument(
        "--mode",
        choices=["visualize", "pattern", "steps"],
        default="visualize",
        help="You may run only the pattern generation or only the steps generation instead of default visualize mode",
    )
    args = parser.parse_args()
    config = get_config(args.wallconfig)
    ptrn = get_pattern(args.brickpattern, config)
    instructions = get_instructions(args.bricksteps, config, ptrn)
    if args.mode == "visualize":
        # I import visualize here because I don't want pygame imported if we aren't in visual mode
        # The problem is that pygame prints a message on import and I don't want this message
        # when the program is used to generate the pattern or the instructions (and you redirect its output to file)
        from lib import visualize

        total_n_bricks = visualize.get_total_n_bricks(ptrn)
        print(
            f"Vizualising laying down {total_n_bricks} bricks in {len(instructions)} strides",
            file=sys.stderr,
        )
        visualize.vizualize(config, ptrn, instructions)
    elif args.mode == "pattern":
        pattern.print_pattern(ptrn)
    elif args.mode == "steps":
        steps.print_instructions(instructions)
