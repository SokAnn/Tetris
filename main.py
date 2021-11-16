"""
GAME TETRIS
"""

import pygame
from random import choice, random
from copy import deepcopy

# globals
W, H = 10, 20  # field size: 10 * 20
square = 30  # square size
screen_resolution = W * square, H * square  # 300, 600
grid = [pygame.Rect(x * square, y * square, square, square) for x in range(W) for y in range(H)]
frame_grid = [pygame.Rect(x * square, y * square, square, square) for x in range(W + 2) for y in range(H + 2)]
next_grid = [pygame.Rect(i * square, j * square, square, square) for i in range(4) for j in range(4)]
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
tetro_color = [(0, 255, 255), (0, 0, 255), (255, 69, 0), (255, 255, 0), (0, 255, 0), (255, 0, 255), (255, 0, 0)]
# for animation
anim_count, anim_speed, anim_limit = 0, 100, 3000
# fonts
pygame.font.init()
title_f = pygame.font.Font('GorgeousPixel.ttf', 50)
title = (title_f.render('T', True, (0, 255, 255)), title_f.render('E', True, (0, 0, 255)),
         title_f.render('T', True, (255, 69, 0)), title_f.render('R', True, (255, 255, 0)),
         title_f.render('I', True, (0, 255, 0)), title_f.render('S', True, (255, 0, 255)))
# info & fonts
score, score_lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
title_score = pygame.font.Font('GorgeousPixel.ttf', 25)
t_s = title_score.render('Score: ', True, (128, 128, 128))
title_lines = pygame.font.Font('GorgeousPixel.ttf', 25)
t_l = title_lines.render('Lines: ', True, (128, 128, 128))
title_record = pygame.font.Font('GorgeousPixel.ttf', 25)
t_r = title_record.render('Record: ', True, (255, 255, 255))


def check_borders():
    if tetromino[i].x < 0 or tetromino[i].x > W - 1:
        return False
    elif tetromino[i].y > H - 1 or field[tetromino[i].y][tetromino[i].x]:
        return False
    return True


if __name__ == "__main__":
    pygame.init()
    # pygame.mixer.init()  # for sounds
    main_surf = pygame.display.set_mode((650, 680))
    frame = pygame.Surface((screen_resolution[0] + 2 * square, screen_resolution[1] + 2 * square))
    frame.set_alpha(255)
    screen = pygame.Surface(screen_resolution)
    screen.set_alpha(255)
    next_surf = pygame.Surface((4 * square, 4 * square))
    next_surf.set_alpha(255)

    # screen = pygame.display.set_mode(screen_resolution)
    pygame.display.update()
    pygame.display.set_caption("TETRIS")
    clock = pygame.time.Clock()

    # main loop
    running = True
    tetromino = deepcopy(choice(tetrominoes))
    color = tetro_color[tetrominoes.index(tetromino)]
    next_tetromino = deepcopy(choice(tetrominoes))
    next_color = tetro_color[tetrominoes.index(next_tetromino)]
    while running:
        main_surf.fill((0, 0, 0))
        [main_surf.blit(title[i_title], (50 + i_title * 30, 10)) for i_title in range(len(title))]
        main_surf.blit(frame, (280, 10))
        main_surf.blit(screen, (310, 40))
        main_surf.blit(next_surf, (80, 105))

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
        # update x (movement)
        tetromino_old = deepcopy(tetromino)
        for i in range(4):
            tetromino[i].x += dx
            if not check_borders():
                tetromino = deepcopy(tetromino_old)
                break
        # update y (movement)
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            for i in range(4):
                tetromino[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[tetromino_old[i].y][tetromino_old[i].x] = color
                    tetromino, color = next_tetromino, next_color
                    next_tetromino = deepcopy(choice(tetrominoes))
                    next_color = tetro_color[tetrominoes.index(next_tetromino)]
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
        # check & deleting lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 10
                lines += 1
        score += scores[lines]  # compute score
        score_lines += lines

        # rendering (visualization)
        [pygame.draw.rect(frame, (128, 128, 128), i_rect) for i_rect in frame_grid]
        [pygame.draw.rect(frame, (40, 40, 40), i_rect, 1) for i_rect in frame_grid]
        screen.fill((0, 0, 0))  # fill background of screen
        [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]
        next_surf.fill((0, 0, 0))
        [pygame.draw.rect(next_surf, (40, 40, 40), i_rect, 1) for i_rect in next_grid]
        # draw temp tetromino
        for i in range(4):
            tetromino_rect.x = tetromino[i].x * square
            tetromino_rect.y = tetromino[i].y * square
            pygame.draw.rect(screen, color, tetromino_rect)
        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    tetromino_rect.x, tetromino_rect.y = x * square, y * square
                    pygame.draw.rect(screen, col, tetromino_rect)
        # draw next tetromino
        for i in range(4):
            tetromino_rect.x = next_tetromino[i].x * square - 10
            tetromino_rect.y = next_tetromino[i].y * square + 135
            pygame.draw.rect(main_surf, next_color, tetromino_rect)

        main_surf.blit(t_s, (50, 260))
        main_surf.blit(t_l, (50, 300))
        main_surf.blit(title_score.render(str(score), True, (128, 128, 128)), (170, 260))
        main_surf.blit(title_lines.render(str(score_lines), True, (128, 128, 128)), (170, 300))
        main_surf.blit(t_r, (50, 340))

        pygame.display.flip()  # flip our screen
        clock.tick(fps)  # check fps

    pygame.quit()
