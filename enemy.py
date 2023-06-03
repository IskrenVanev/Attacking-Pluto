import pygame
import sys
import random
import time
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Enemy(pygame.sprite.Sprite):
    SCORE = 0
    enemy_bat_images = [
            "img/Enemies/EnemyLvl1 animated/Bat1.png",
            "img/Enemies/EnemyLvl1 animated/Bat2.png",
            "img/Enemies/EnemyLvl1 animated/Bat3.png"
        ]
    enemy_eye_images = [
            "img/Enemies/EnemyLvl1 animated/eye1.png",
            "img/Enemies/EnemyLvl1 animated/eye2.png",
            "img/Enemies/EnemyLvl1 animated/eye3.png"
        ]
    enemy_dragon_images = [
            "img/Enemies/EnemyLvl1 animated/dragon1.png",
            "img/Enemies/EnemyLvl1 animated/dragon2.png",
            "img/Enemies/EnemyLvl1 animated/dragon3.png"
        ]
    def __init__(self):
        super().__init__()
       
       
  
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
       # self.is_frozen = False
        self.pause = 0
 
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
            
    # @staticmethod
    # def freeze_all(enemies):
    #     for enemy in enemies:
    #         enemy.is_frozen = True

    #     start_time = time.time()
    #     while time.time() - start_time < 0.5:  # Freeze for 0.5 seconds
    #         pygame.time.wait(10)  # Adjust the delay time if needed

    #     for enemy in enemies:
    #         enemy.is_frozen = False
    # def freeze(self):
    #     self.is_frozen = True
    #     start_time = time.time()
    #     while time.time() - start_time < 0.1:  # Freeze for 0.5 seconds
    #         pygame.time.wait(1)  # Adjust the delay time if needed
    #     self.is_frozen = False

    def update(self):
        if self.pause:
            self.pause -= 1
            return       
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
    def collide_with_player(self):
        self.pause = 70  # Pause for 30 frames (adjust as needed)

    def get_pause(self):
        return self.pause
    def set_pause(self, value):
        self.pause = value