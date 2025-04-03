import math
import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DISPLAY_OFFSET = 20

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

WALL_WIDTH = 2300
WALL_HEIGHT = 2000
BRICK_HEIGHT = 50
BRICK_WIDTH = 210
HEAD_JOINT = 10
COURSE_HEIGHT = 62.5

wall = pygame.Surface((WALL_WIDTH, WALL_HEIGHT))
wall.fill("white")
n_courses = int(math.ceil(WALL_HEIGHT / COURSE_HEIGHT))

for i in range(n_courses):
    x = 0
    while x < WALL_WIDTH:
        pygame.draw.rect(
            wall, "gray", (x, i * COURSE_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        )
        x += BRICK_WIDTH + HEAD_JOINT


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH = event.w
            SCREEN_HEIGHT = event.h
            screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
            )
            if SCREEN_WIDTH < DISPLAY_OFFSET * 3 or SCREEN_HEIGHT < DISPLAY_OFFSET * 3:
                print("Warning: Window size too small, the wall won't be displayed")

    if SCREEN_WIDTH >= DISPLAY_OFFSET * 3 and SCREEN_HEIGHT >= DISPLAY_OFFSET * 3:
        displayed_wall = pygame.transform.flip(wall, flip_x=False, flip_y=True)
        width = SCREEN_WIDTH - 2 * DISPLAY_OFFSET
        height = width * WALL_HEIGHT / WALL_WIDTH
        if height > SCREEN_HEIGHT - 2 * DISPLAY_OFFSET:
            height = SCREEN_HEIGHT - 2 * DISPLAY_OFFSET
            width = height * WALL_WIDTH / WALL_HEIGHT
        displayed_wall = pygame.transform.scale(displayed_wall, (width, height))
        screen.blit(
            displayed_wall, ((SCREEN_WIDTH - width) / 2, (SCREEN_HEIGHT - height) / 2)
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
