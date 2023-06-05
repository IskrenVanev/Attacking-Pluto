import pygame
import sys
import random


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
class Boss_Bullet(pygame.sprite.Sprite):
    def __init__(self, x , y):#x and y represent the center of the ship
        super().__init__()
        self.image = pygame.image.load("img\Bullet_enemy.png")
        
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = -5
        
        
    def update(self):
        self.rect.y -=self.speed_y

        if self.rect.bottom < 0:
            self.kill()