"""
GAME TETRIS
"""

import pygame
from random import choice, random
from copy import deepcopy

# globals
W, H = 10, 20  # field size: 10 * 20
square = 30  # square size
screen_resolution = W * square, H * square
grid = [pygame.Rect(x * square, y * square, square, square) for x in range(W) for y in range(H)]
field = [[0 for i in range(W)] for j in range(H)]
fps = 100  # frame rate
# tetrominoes
I = [(-1, 0), (-2, 0), (0, 0), (1, 0)]
J = [(0, 0), (-1, -1), (-1, 0), (1, 0)]
L = [(0, 0), (-2, 0), (-1, 0), (0, -1)]
O = [(0, -1), (-1, -1), (-1, 0), (0, 0)]
S = [(0, 0), (-1, 0), (0, -1), (1, -1)]
T = [(0, 0), (-1, 0), (0, -1), (1, 0)]
Z = [(0, 0), (-1, -1), (0, -1), (1, 0)]
tetrominoes_pos = [I, J, L, O, S, T, Z]
tetrominoes = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in t_pos] for t_pos in tetrominoes_pos]
tetromino_rect = pygame.Rect(0, 0, square - 2, square - 2)
tetro_color = [(0, 255, 255), (0, 0, 255), (255, 69, 0), (255, 255, 0),
               (0, 255, 0), (255, 0, 255), (255, 0, 0)]
# for animation
anim_count, anim_speed, anim_limit = 0, 60, 2000


def check_borders():
    if tetromino[i].x < 0 or tetromino[i].x > W - 1:
        return False
    elif tetromino[i].y > H - 1 or field[tetromino[i].y][tetromino[i].x]:
        return False
    return True


if __name__ == "__main__":
    pygame.init()
    # pygame.mixer.init()  # for sounds
    screen = pygame.display.set_mode(screen_resolution)
    pygame.display.set_caption("TETRIS")
    clock = pygame.time.Clock()

    # main loop
    running = True
    tetromino = deepcopy(choice(tetrominoes))
    color = tetro_color[tetrominoes.index(tetromino)]
    while running:
        clock.tick(fps)  # loop speed
        dx = 0
        rotate = False
        # event
        for event in pygame.event.get():
            # check event (closing window)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # check event (press button left)
                if event.key == pygame.K_LEFT:
                    dx = -1
                # check event (press button right)
                if event.key == pygame.K_RIGHT:
                    dx = 1
                # check event (press button space)
                if event.key == pygame.K_SPACE:
                    rotate = True
                # check event (press button down)
                if event.key == pygame.K_DOWN:
                    anim_limit = 100

        # update information for animation (update positions)
        # update x
        tetromino_old = deepcopy(tetromino)
        for i in range(4):
            tetromino[i].x += dx
            if not check_borders():
                tetromino = deepcopy(tetromino_old)
                break
        # update y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            for i in range(4):
                tetromino[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[tetromino_old[i].y][tetromino_old[i].x] = color
                    tetromino = deepcopy(choice(tetrominoes))
                    color = tetro_color[tetrominoes.index(tetromino)]
                    anim_limit = 2000
                    break
        # rotation
        tetromino_old = deepcopy(tetromino)
        center = tetromino[0]
        if rotate:
            for i in range(4):
                x = tetromino[i].y - center.y
                y = tetromino[i].x - center.x
                tetromino[i].x = center.x - x
                tetromino[i].y = center.y + y
                if not check_borders():
                    tetromino = deepcopy(tetromino_old)
                    break
        # deleting lines
        line = H - 1
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1

        # rendering (visualization)
        screen.fill((0, 0, 0))  # fill background of screen
        [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

        for i in range(4):
            tetromino_rect.x = tetromino[i].x * square
            tetromino_rect.y = tetromino[i].y * square
            pygame.draw.rect(screen, color, tetromino_rect)
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    tetromino_rect.x, tetromino_rect.y = x * square, y * square
                    pygame.draw.rect(screen, col, tetromino_rect)

        pygame.display.flip()  # flip our screen
        clock.tick(fps)  # check fps

    pygame.quit()
