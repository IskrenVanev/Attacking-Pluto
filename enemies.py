
import pygame
import sys
from pygame.locals import *
import random
SCREEN_WIDTH = 1200
SPEED = 5
SCORE = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemies\BigBat2.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)
        

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 1200):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(90, 900), 0)