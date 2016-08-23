import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('play music')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
fontObj = pygame.font.Font('freesansbold.ttf', 32)
textObj = fontObj.render('Now playing~~', True, GREEN, BLUE)



pygame.mixer.init()
pygame.mixer.music.load('nexttoyou.mp3')
pygame.mixer.music.play(-1, 0.0)

while True:
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('play music @ ' + str(pygame.mixer.music.get_pos()))

    for eve in pygame.event.get():
        if eve.type == QUIT:
            pygame.quit()
            sys.exit()
        elif eve.type == KEYDOWN:
            if eve.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif eve.key == K_p:
                pygame.mixer.music.pause()
            elif eve.key == K_s:
                pygame.mixer.music.unpause()
            elif eve.key == K_r:
                pygame.mixer.music.rewind()
            elif eve.key == K_UP:
                t = pygame.mixer.music.get_volume()
                t = t + .10
                if t > 1.0:
                    t = 1.0
                pygame.mixer.music.set_volume(t)
            elif eve.key == K_DOWN:
                t = pygame.mixer.music.get_volume()
                t = t - .1
                if t < 0.0:
                    t = 0.0
                pygame.mixer.music.set_volume(t)

    pygame.display.update()

