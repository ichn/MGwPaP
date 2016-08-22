import pygame, sys
from pygame.locals import *
import time

FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

while True:
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('Animation' + str(fpsClock))
    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'

    if direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'

    if direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'

    if direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
#    time.sleep(.01)
    fpsClock.tick(FPS)
