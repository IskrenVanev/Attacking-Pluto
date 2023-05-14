import pygame
import sys
import random
import random, time
import bullet
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080



class Player(pygame.sprite.Sprite):
    def __init__(self,all_bullets, all_sprites):
        super().__init__()
        self.image = pygame.image.load("img\Player\spaceship_black.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        cropped_height = int(self.image.get_height() * 0.8)
        self.image = self.image.subsurface(pygame.Rect(0, 0, self.image.get_width(), cropped_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.bottom = SCREEN_HEIGHT-10
        self.speed_x=0
        self.speed = 8
        self.all_bullets = all_bullets
        self.all_sprites = all_sprites
        self.last_bullet_shot = pygame.time.get_ticks()

       
    def shoot_bullet(self):
        #shoot bullet when space is pressed
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot > 200:
            self.last_bullet_shot = current_time
            b = bullet.Bullet(self.rect.centerx, self.rect.top)
            self.all_bullets.add(b)
            self.all_sprites.add(b)

    def boundary(self):
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def movement(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speed_x = self.speed
        if keystate[pygame.K_LEFT]:
            self.speed_x = -self.speed    #8 pixels to the left
        if keystate[pygame.K_SPACE]:
            self.shoot_bullet()
        self.rect.x += self.speed_x
          
    def update(self):
        self.movement()
        self.boundary()         