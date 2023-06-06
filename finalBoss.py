import pygame
import sys
import random
import time
from finalBossBullet import Boss_Bullet
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
#SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
class Boss(pygame.sprite.Sprite):
    SCORE = 0
    enemy_boss_images = [
            "img/Enemies/FinalBoss/Boss1.png",
            "img/Enemies/FinalBoss/Boss2.png"
            
        ]
   
    def __init__(self,all_bullets, all_sprites):
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

        self.life_points = 20  

        self.all_bullets = all_bullets
        self.all_sprites = all_sprites
        self.direction = random.choice([-1, 1])  # Randomly choose left (-1) or right (1)
        self.speed = random.randint(1, 5)  # Random speed between 1 and 5
        self.change_direction_chance = 0.01 



    def update_movement(self):
        if random.random() < self.change_direction_chance:
            self.direction *= -1  # Reverse the direction

        self.rect.x += self.direction * self.speed

        # Check if the boss reached the screen edges and change direction if needed
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1  # Reverse the direction
    



    def shoot_bullet(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot >= 1000:  # Shoot a bullet every 1 second (adjust as needed)
            bullet1 = Boss_Bullet(self.rect.centerx, self.rect.bottom)
            bullet2 = Boss_Bullet(self.rect.centerx - 100, self.rect.bottom)  # Adjust bullet positions as needed
            bullet3 = Boss_Bullet(self.rect.centerx + 100, self.rect.bottom)  # Adjust bullet positions as needed

            bullet1.set_direction(random.choice([-4,4]))  # Set random direction for each bullet
            bullet2.set_direction(random.choice([-4,4]))  # Set random direction for each bullet
            bullet3.set_direction(random.choice([-4,4]))  # Set random direction for each bullet

            self.all_bullets.add(bullet1, bullet2, bullet3)
            self.all_sprites.add(bullet1, bullet2, bullet3)

            self.last_bullet_shot = current_time



    def draw_life_bar(self):
        screen = pygame.display.get_surface()
        # Calculate the width of the life bar based on the remaining life points
        bar_width = self.life_points * 20  # Assuming each life point is represented by a bar of width 20
        bar_height = 10
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 5  # Position the life bar above the boss sprite

        # Draw the life bar
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))




    def update(self):
        self.update_movement()
        
        self.shoot_bullet()
        
        # Animation
        self.change_image_timer += 1
        if self.change_image_timer >= 30:  # Change image every 10 frames (adjust as needed)
            self.image_index = (self.image_index + 1) % len(self.enemy_images)  # Cycle through the images
            self.image = pygame.image.load(self.enemy_images[self.image_index])
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 3), int(self.image.get_height() * 3)))  # Adjust scale factor here
            self.change_image_timer = 0
        if self.life_points <= 0:
            self.kill()
        self.draw_life_bar()