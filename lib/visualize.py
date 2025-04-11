import sys

import pygame

from .pattern import get_total_n_bricks
from .steps import Stride, brick_bottom_left


# There is no direct hsla color constructor in pygame, so I made a function for it
def hsl_color(h: float, s: float, l: float) -> pygame.Color:
    color = pygame.Color(0, 0, 0)
    color.hsla = (h, s, l)
    return color


def get_current_stride_n(n_layed_bricks: int, instructions: list[Stride]) -> int:
    i = n_layed_bricks
    current_stride_n = 0
    while i > len(instructions[current_stride_n].steps):
        i -= len(instructions[current_stride_n].steps)
        current_stride_n += 1
    return current_stride_n


def create_wall(
    config: dict,
    ptrn: list[list[str]],
    instructions: list[Stride],
    n_layed_bricks: int,
) -> pygame.Surface:
    # initialize font for rendering stride numbers

    DEFAULT_FONT = pygame.font.SysFont(pygame.font.get_default_font(), 50)

    # Create the Surface for the wall, fill it with white

    wall_width = config["wall"]["width"]
    wall_height = config["wall"]["height"]

    wall = pygame.Surface((wall_width, wall_height))
    wall.fill("white")

    # Draw the envelope

    current_stride_n = get_current_stride_n(n_layed_bricks, instructions)
    envelope_left_x = instructions[current_stride_n].envelope_pos.x
    envelope_bottom_y = instructions[current_stride_n].envelope_pos.y
    envelope_width = config["envelope"]["width"]
    envelope_height = config["envelope"]["height"]

    # In my coordinate system (0, 0) is at the bottom left of the wall
    # x goes right, y goes up
    # In pygame (0, 0) is at the top left of the window
    # x goes right, y goes down
    # I have to pass the top left corner of the rectangle to draw it
    # So to convert "bottom left corner in my system" to "top left corner in pygame"
    # I have to do the following math
    envelope_y = wall_height - envelope_bottom_y - envelope_height
    pygame.draw.rect(
        wall,
        hsl_color(0, 0, 20),
        (
            envelope_left_x,
            envelope_y,
            envelope_width,
            envelope_height,
        ),
    )

    # Draw bricks

    brick_n = 0
    for stride_n, stride in enumerate(instructions):
        for brick_pos in stride.steps:
            brick_bottom_left_coords = brick_bottom_left(brick_pos, config, ptrn)
            brick_type = ptrn[brick_pos.y][brick_pos.x]
            brick_length = config["bricks"][brick_type]["length"]
            brick_height = config["bricks"][brick_type]["height"]
            # layed bricks have lightness 30 (dark), unlayed bricks have lightnes 80 (light)
            brick_color = (
                hsl_color(0, 0, 30) if brick_n < n_layed_bricks else hsl_color(0, 0, 80)
            )
            pygame.draw.rect(
                wall,
                brick_color,
                (
                    brick_bottom_left_coords.x,
                    # Same coordinate systems conversion math as with the envelope
                    wall_height - brick_bottom_left_coords.y - brick_height,
                    brick_length,
                    brick_height,
                ),
            )
            number = DEFAULT_FONT.render(str(stride_n + 1), False, hsl_color(0, 0, 100))
            wall.blit(
                number,
                (
                    # Just some math to put the number in the middle of the brick
                    brick_bottom_left_coords.x
                    + brick_length / 2
                    - (number.get_width() / 2),
                    wall_height
                    - brick_bottom_left_coords.y
                    - brick_height / 2
                    - (number.get_height() / 2),
                ),
            )
            brick_n += 1

    return wall


def vizualize(config: dict, ptrn: list[list[str]], instructions: list[Stride]):

    # variables for window size and padding

    window_width = 1280  # initial window width; can be resized
    window_height = 720  # initial window height; can be resized
    window_padding = 20  # padding between the edge of the window and the visualization

    # Initializing pygame

    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # variables for the bricks

    total_n_bricks = get_total_n_bricks(ptrn)  # total amount of bricks
    n_layed_bricks = 0  # current amount of layed (dark) bricks

    # Starting the "game" loop

    running = True
    while running:

        # Handling events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                window_width = event.w
                window_height = event.h
                screen = pygame.display.set_mode(
                    (window_width, window_height), pygame.RESIZABLE
                )
                if (
                    window_width < window_padding * 3
                    or window_height < window_padding * 3
                ):
                    print(
                        "Warning: Window size too small, the wall won't be displayed",
                        file=sys.stderr,
                    )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    n_layed_bricks += 1
                    if n_layed_bricks > total_n_bricks:
                        n_layed_bricks = total_n_bricks
                elif event.key == pygame.K_BACKSPACE:
                    n_layed_bricks -= 1
                    if n_layed_bricks < 0:
                        n_layed_bricks = 0

        # Actually creating the visualization of the wall

        wall = create_wall(config, ptrn, instructions, n_layed_bricks)

        # Put the visualization on screen taking the window resizing into account

        if window_width >= window_padding * 3 and window_height >= window_padding * 3:
            width = window_width - 2 * window_padding
            height = width * wall.get_height() / wall.get_width()
            if height > window_height - 2 * window_padding:
                height = window_height - 2 * window_padding
                width = height * wall.get_width() / wall.get_height()
            displayed_wall = pygame.transform.scale(wall, (width, height))
            screen.blit(
                displayed_wall,
                ((window_width - width) / 2, (window_height - height) / 2),
            )
        pygame.display.flip()

        # Limiting to 60 FPS; pygame practice

        clock.tick(60)

    pygame.quit()
