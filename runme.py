import argparse
import tomllib

from lib import pattern, steps, vizualize

def arrange_data_for_visualisation() -> (
    tuple[dict, list[list[str]], list[steps.Stride]]
):
    parser = argparse.ArgumentParser(
        prog="Vizualise bricks",
        description="Visualises laying down different bonds of bricks",
    )
    parser.add_argument("--wallconfig")
    args = parser.parse_args()
    wallconfig = args.wallconfig if args.wallconfig else "stretcher_bond.wallconfig"
    with open(wallconfig, "rb") as configfile:
        config = tomllib.load(configfile)
        ptrn = pattern.get_pattern(config)
        instructions = steps.get_instructions(config, ptrn)
        return config, ptrn, instructions
    print("Error: couldn't load data for visualisation", file=sys.stderr)
    exit(1)

if __name__ == "__main__":

    config, ptrn, instructions = arrange_data_for_visualisation()
    total_n_bricks = vizualize.get_total_n_bricks(ptrn)
    print(
        f"Vizualising laying down {total_n_bricks} bricks in {len(instructions)} strides"
    )
    vizualize.vizualize(config, ptrn, instructions)