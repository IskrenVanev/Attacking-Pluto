import pygame
import sys
import random

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Enemy(pygame.sprite.Sprite):
    SCORE = 0
    def __init__(self):
        super().__init__()
        self.enemy_bat_images = [
            "img/Enemies/EnemyLvl1 animated/Bat1.png",
            "img/Enemies/EnemyLvl1 animated/Bat2.png",
            "img/Enemies/EnemyLvl1 animated/Bat3.png"
        ]
        self.enemy_eye_images = [
            "img/Enemies/EnemyLvl1 animated/eye1.png",
            "img/Enemies/EnemyLvl1 animated/eye2.png",
            "img/Enemies/EnemyLvl1 animated/eye3.png"
        ]
        self.enemy_dragon_images = [
            "img/Enemies/EnemyLvl1 animated/dragon1.png",
            "img/Enemies/EnemyLvl1 animated/dragon2.png",
            "img/Enemies/EnemyLvl1 animated/dragon3.png"
        ]
       
  
        self.enemy_images = random.choice([self.enemy_bat_images, self.enemy_eye_images, self.enemy_dragon_images])  # Choose a random set of enemy images
        
        self.image = pygame.image.load(self.enemy_images[0])
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)
        self.image_index = 0  # Current image index for animation
        self.change_image_timer = 0  # Timer to control image change

    def spawn_new_enemy(self):
        
        Enemy.SCORE+=1
        self.enemy_images = random.choice([self.enemy_bat_images, self.enemy_eye_images, self.enemy_dragon_images])  # Choose a random set of enemy images
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)
        

    def boundary(self):
        
        if self.rect.left > SCREEN_WIDTH +5 or self.rect.right < -5 or self.rect.top > SCREEN_HEIGHT + 5: 
               
            self.spawn_new_enemy()

    def update(self):       
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.boundary()

        # Animation
        self.change_image_timer += 1
        if self.change_image_timer >= 10:  # Change image every 10 frames (adjust as needed)
            self.image_index = (self.image_index + 1) % len(self.enemy_images)  # Cycle through the images
            self.image = pygame.image.load(self.enemy_images[self.image_index])
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))
            self.change_image_timer = 0