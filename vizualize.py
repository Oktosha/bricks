import math
import pygame
import tomllib
import sys

import pattern
import steps
import geom

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DISPLAY_OFFSET = 20


def arrange_data_for_visualisation() -> (
    tuple[dict, list[list[str]], list[steps.Stride]]
):
    with open("stretcher_bond.wallconfig", "rb") as configfile:
        config = tomllib.load(configfile)
        ptrn = pattern.get_pattern(config)
        instructions = steps.get_instructions(config, ptrn)
        return config, ptrn, instructions
    print("Error: couldn't load data for visualisation", file=sys.stderr)
    exit(1)


def get_total_n_bricks(ptrn: list[list[str]]):
    return sum(map(len, ptrn))


def draw_wall(
    config: dict,
    ptrn: list[list[str]],
    instructions: list[steps.Stride],
    n_layed_bricks: int,
):
    DEFAULT_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 50)

    wall_width = config["wall"]["width"]
    wall_height = config["wall"]["height"]

    wall = pygame.Surface((wall_width, wall_height))
    wall.fill("white")

    i = n_layed_bricks
    stride = 0
    while i > len(instructions[stride].steps):
        i -= len(instructions[stride].steps)
        stride += 1
    envelope_color = pygame.Color(0, 0, 0)
    envelope_color.hsla = (0, 0, 20)
    pygame.draw.rect(
        wall,
        envelope_color,
        (
            instructions[stride].envelope_pos.x,
            wall_height
            - instructions[stride].envelope_pos.y
            - config["envelope"]["height"],
            config["envelope"]["width"],
            config["envelope"]["height"],
        ),
    )

    brick_n = 0
    for stride_n, stride in enumerate(instructions):
        for brick_pos in stride.steps:
            brick_bottom_left_coords = geom.bottom_left_coordinates_of_a_brick(
                brick_pos, config, ptrn
            )
            brick_type = ptrn[brick_pos.y][brick_pos.x]
            brick_length = config["bricks"][brick_type]["length"]
            brick_height = config["bricks"][brick_type]["height"]
            brick_color = pygame.Color(0, 0, 0)
            brick_font_color = pygame.Color(0, 0, 0)
            if brick_n < n_layed_bricks:
                brick_color.hsla = (0, 0, 30)
                brick_font_color.hsla = (0, 0, 100)
            else:
                brick_color.hsla = (0, 0, 80)
                brick_font_color.hsla = (0, 0, 100)
            pygame.draw.rect(
                wall,
                brick_color,
                (
                    brick_bottom_left_coords.x,
                    wall_height - brick_bottom_left_coords.y - brick_height,
                    brick_length,
                    brick_height,
                ),
            )
            number = DEFAULT_FONT.render(str(stride_n + 1), False, brick_font_color)
            wall.blit(
                number,
                (
                    brick_bottom_left_coords.x + brick_length / 2,
                    wall_height - brick_bottom_left_coords.y - brick_height + 8,
                ),
            )
            brick_n += 1

    return wall


if __name__ == "__main__":

    config, ptrn, instructions = arrange_data_for_visualisation()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    total_n_bricks = get_total_n_bricks(ptrn)
    n_layed_bricks = 0

    print(
        f"Vizualising laying down {total_n_bricks} bricks in {len(instructions)} strides"
    )

    while running:

        # Handling events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
                )
                if (
                    SCREEN_WIDTH < DISPLAY_OFFSET * 3
                    or SCREEN_HEIGHT < DISPLAY_OFFSET * 3
                ):
                    print("Warning: Window size too small, the wall won't be displayed")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    n_layed_bricks += 1
                    if n_layed_bricks > total_n_bricks:
                        n_layed_bricks = total_n_bricks
                elif event.key == pygame.K_BACKSPACE:
                    n_layed_bricks -= 1
                    if n_layed_bricks < 0:
                        n_layed_bricks = 0

        # Call the vizualisation function

        wall = draw_wall(config, ptrn, instructions, n_layed_bricks)

        # Put the vizualisation on screen accounting for the window resizing

        if SCREEN_WIDTH >= DISPLAY_OFFSET * 3 and SCREEN_HEIGHT >= DISPLAY_OFFSET * 3:
            width = SCREEN_WIDTH - 2 * DISPLAY_OFFSET
            height = width * wall.get_height() / wall.get_width()
            if height > SCREEN_HEIGHT - 2 * DISPLAY_OFFSET:
                height = SCREEN_HEIGHT - 2 * DISPLAY_OFFSET
                width = height * wall.get_width() / wall.get_height()
            displayed_wall = pygame.transform.scale(wall, (width, height))
            screen.blit(
                displayed_wall,
                ((SCREEN_WIDTH - width) / 2, (SCREEN_HEIGHT - height) / 2),
            )
        pygame.display.flip()

        # Limiting to 60 FPS; pygame practice

        clock.tick(60)

    pygame.quit()
