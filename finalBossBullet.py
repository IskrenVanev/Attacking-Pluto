import pygame
import sys
import random


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
class Boss_Bullet(pygame.sprite.Sprite):
    def __init__(self, x , y):#x and y represent the center of the ship
        super().__init__()
        self.frames = [
            pygame.image.load("img/Enemies/FinalBoss/GreenOrb1.png"),
            pygame.image.load("img/Enemies/FinalBoss/GreenOrb2.png"),
            pygame.image.load("img/Enemies/FinalBoss/GreenOrb3.png"),
            # Add more frames here if needed
        ]
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speed_y = -3
        self.animation_timer = 0
        self.animation_delay = 10  
        self.direction = 0
        
    def set_direction(self, direction):
        self.direction = direction    
    def update(self):
       
        self.rect.y -=self.speed_y
        self.rect.x += self.direction
        if self.rect.bottom < 0 or self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()
        
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            self.animation_timer = 0
        #self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))