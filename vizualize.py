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

    wall_width = config["wall"]["width"]
    wall_height = config["wall"]["height"]

    wall = pygame.Surface((wall_width, wall_height))
    wall.fill("white")

    for course_n in range(len(ptrn)):
        for x_pos in range(len(ptrn[course_n])):
            brick_bottom_left_coords = geom.bottom_left_coordinates_of_a_brick(
                geom.PositionInPattern(x_pos, course_n), config, ptrn
            )
            brick_length = config["bricks"][ptrn[course_n][x_pos]]["length"]
            brick_height = config["bricks"][ptrn[course_n][x_pos]]["height"]
            pygame.draw.rect(
                wall,
                "gray",
                (
                    brick_bottom_left_coords.x,
                    brick_bottom_left_coords.y,
                    brick_length,
                    brick_height,
                ),
            )

    return wall


if __name__ == "__main__":

    config, ptrn, instructions = arrange_data_for_visualisation()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    total_n_bricks = get_total_n_bricks(ptrn)
    n_layed_bricks = 0

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
            displayed_wall = pygame.transform.flip(wall, flip_x=False, flip_y=True)
            width = SCREEN_WIDTH - 2 * DISPLAY_OFFSET
            height = width * wall.get_height() / wall.get_width()
            if height > SCREEN_HEIGHT - 2 * DISPLAY_OFFSET:
                height = SCREEN_HEIGHT - 2 * DISPLAY_OFFSET
                width = height * wall.get_width() / wall.get_height()
            displayed_wall = pygame.transform.scale(displayed_wall, (width, height))
            screen.blit(
                displayed_wall,
                ((SCREEN_WIDTH - width) / 2, (SCREEN_HEIGHT - height) / 2),
            )
        pygame.display.flip()

        # Limiting to 60 FPS; pygame practice

        clock.tick(60)

    pygame.quit()
