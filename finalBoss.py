import pygame
import sys
import random
import time
from finalBossBullet import Boss_Bullet
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Boss(pygame.sprite.Sprite):
    SCORE = 0
    enemy_boss_images = [
            "img/Enemies/FinalBoss/Boss1.png",
            "img/Enemies/FinalBoss/Boss2.png"
            
        ]
   
    def __init__(self):
        super().__init__()

        self.enemy_images = self.enemy_boss_images

        self.image = pygame.image.load("img/Enemies/FinalBoss/Boss1.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2  # Set boss position at the middle of the screen horizontally
        self.rect.y = 10  # Set boss position at the upper side of the screen
        self.image_index = 0  # Current image index for animation
        self.change_image_timer = 0  # Timer to control image change
        self.last_bullet_shot = pygame.time.get_ticks()  # Initialize last bullet shot time

        self.all_bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def shoot_bullet(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot >= 1000:  # Shoot a bullet every 1 seconds (adjust as needed)
            bullet = Boss_Bullet(self.rect.centerx, self.rect.bottom)
            self.all_bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.last_bullet_shot = current_time



    def update(self):
       
        
        
        self.shoot_bullet()
        # Animation
        self.change_image_timer += 1
        if self.change_image_timer >= 10:  # Change image every 10 frames (adjust as needed)
            self.image_index = (self.image_index + 1) % len(self.enemy_images)  # Cycle through the images
            self.image = pygame.image.load(self.enemy_images[self.image_index])
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))  # Adjust scale factor here
            self.change_image_timer = 0
