"""
GAME TETRIS
"""

import pygame
import random

# global
width = 800
height = 700
pf_width = 300  # playing field: width
pf_height = 600  # playing field: height
fps = 30  #
top_x = width - pf_width  #
top_y = height - pf_height
# tetrominoes
I = [['....',
      '****',
      '....',
      '....'],
     ['..*.',
      '..*.',
      '..*.',
      '..*.']]
J = [['....',
      '.***',
      '...*',
      '....'],
     ['..*.',
      '..*.',
      '.**.',
      '....'],
     ['.*..',
      '.***',
      '....',
      '....'],
     ['..**',
      '..*.',
      '..*.',
      '....']]
L = [['....',
      '.***',
      '.*..',
      '....'],
     ['.**.',
      '..*.',
      '..*.',
      '....'],
     ['...*',
      '.***',
      '....',
      '....'],
     ['..*.',
      '..*.',
      '..**',
      '....']]
O = ['....',
     '.**.',
     '.**.',
     '....']
S = [['....',
      '..**',
      '.**.',
      '....'],
     ['.*..',
      '.**.',
      '..*.',
      '....']]
T = [['....',
      '.***',
      '..*.',
      '....'],
     ['..*.',
      '.**.',
      '..*.',
      '....'],
     ['..*.',
      '.***',
      '....',
      '...'],
     ['..*.',
      '..**',
      '..*.',
      '....']]
Z = [['....',
      '.**.',
      '..**',
      '....'],
     ['..*.',
      '.**.',
      '.*..',
      '....']]
tetrominoes = [I, J, L, O, S, T, Z]
tetro_color = [(0, 0, 255), (0, 0, 139), (255, 165, 0), (255, 255, 0), (0, 255, 0), (255, 0, 255), (255, 0, 0)]

#
# class Sprite:
#     pass


if __name__ == "__main__":
    pygame.init()
    # pygame.mixer.init()  # for sounds
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("TETRIS")
    clock = pygame.time.Clock()

    # main loop
    running = True
    while running:
        clock.tick(fps)  # loop speed
        # event
        for event in pygame.event.get():
            # check event (closing window)
            if event.type == pygame.QUIT:
                running = False
        # update

        # rendering (visualization)
        screen.fill((0, 0, 0))  # fill background of screen
        pygame.display.flip()  # flip our screen

    pygame.quit()
