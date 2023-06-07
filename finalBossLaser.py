import pygame
import sys
import random


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Boss_Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, boss):  # x and y represent the center of the ship
        super().__init__()
        self.image = pygame.image.load("img/Enemies/FinalBoss/BigLaser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.follow_boss = True
        self.boss = boss
        

    def set_direction(self, direction):
        self.direction = direction

    def update(self):
        self.rect.centerx = self.boss.rect.centerx  # Set the laser's x-coordinate to the boss's x-coordinate
        self.rect.bottom = self.boss.rect.bottom
        
        
        