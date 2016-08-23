import pygame, sys, time
from pygame.locals import *

#pygame.init() i want to fuck my self....
pygame.mixer.init()
pygame.mixer.music.load('nexttoyou.mp3')
pygame.mixer.music.play(-1, 0.0)
while True:
    pass
while pygame.mixer.music.get_busy():
    pygame.time.delay(100)
    pass
