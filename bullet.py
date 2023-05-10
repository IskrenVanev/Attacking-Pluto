import pygame
import sys
import random
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x , y):#x and y represent the center of the ship
        super().__init__()
        self.image = pygame.image.load("img\Player\Bullets\laserRed01.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = -10

        #self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        #self.rect.y = random.randrange(-150,-100)
        #self.speed_y = random.randrange(2,8)
        #self.speed_x = random.randrange(-3,3)
        
    def update(self):
        self.rect.y +=self.speed_y

        if self.rect.bottom < 0:
            self.kill()