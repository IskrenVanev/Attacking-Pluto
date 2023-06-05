import pygame
import sys
import random
import time
import math
from alien_bullets import Bullet

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Enemy2(pygame.sprite.Sprite):
    SCORE = 0
    enemy_alien_spaceship_ver1 = [
            "img/Enemies/lvl2aliens/ship (1).png",
            "img/Enemies/lvl2aliens/ship (2).png",
            "img/Enemies/lvl2aliens/ship (3).png"
        ]
    enemy_alien_spaceship_ver2 = [
            "img/Enemies/lvl2aliens/ship (4).png",
            "img/Enemies/lvl2aliens/ship (5).png",
            "img/Enemies/lvl2aliens/ship (6).png"
        ]

    def __init__(self,all_bullets, all_sprites):
        super().__init__()

        self.enemy_images = random.choice([self.enemy_alien_spaceship_ver1, self.enemy_alien_spaceship_ver2])  # Choose a random set of enemy images

        self.image = pygame.image.load(self.enemy_images[0])
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))  # Adjust scale factor here
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(2, 8)
        self.speed_x = random.randrange(-3, 3)
        self.image_index = 0  # Current image index for animation
        self.change_image_timer = 0  # Timer to control image change
        self.pause = 0
        self.all_bullets = all_bullets
        self.all_sprites = all_sprites
        
        self.last_bullet_shot = pygame.time.get_ticks()
    def spawn_new_enemy(self):
        Enemy2.SCORE += 1
        self.enemy_images = random.choice([self.enemy_alien_spaceship_ver1, self.enemy_alien_spaceship_ver2])  # Choose a random set of enemy images
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(2, 8)
        self.speed_x = random.randrange(-3, 3)

    def boundary(self):
        if self.rect.left > SCREEN_WIDTH + 5 or self.rect.right < -5 or self.rect.top > SCREEN_HEIGHT + 5:
            self.spawn_new_enemy()



    def shoot_bullet(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot >= 1000:  # Shoot a bullet every 1 seconds (adjust as needed)
            bullet = Bullet(self.rect.centerx, self.rect.bottom)
            self.all_bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.last_bullet_shot = current_time



    def update(self):
        if self.pause:
            self.pause -= 1
            return
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.boundary()
        self.shoot_bullet()
        # Animation
        self.change_image_timer += 1
        if self.change_image_timer >= 10:  # Change image every 10 frames (adjust as needed)
            self.image_index = (self.image_index + 1) % len(self.enemy_images)  # Cycle through the images
            self.image = pygame.image.load(self.enemy_images[self.image_index])
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))  # Adjust scale factor here
            self.change_image_timer = 0

    def collide_with_player(self):
        self.pause = 70  # Pause for 30 frames (adjust as needed)

    def get_pause(self):
        return self.pause

    def set_pause(self, value):
        self.pause = value