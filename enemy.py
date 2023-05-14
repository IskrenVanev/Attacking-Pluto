
import pygame
import sys
import random

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
#SPEED_Y=5
class Enemy(pygame.sprite.Sprite):
  
    
    def __init__(self):
        super().__init__()
        enemy_images = [
            "img/Enemies/BigBat2.png",
            "img/Enemies/fish01Nobg.png",
            "img/Enemies/flappybird.png"
        ]
        random_image_path = random.choice(enemy_images)
        self.image = pygame.image.load(random_image_path)
        #self.image = pygame.image.load("img\Enemies\BigBat2.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)
        #self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)
       # self.score = 0
       # self.speed_y = random.randrange(2,8)
        #self.speed_x = random.randrange(-5,5)

    def spawn_new_enemy(self):
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)

    def boundary(self):
        if self.rect.left > SCREEN_WIDTH +5 or self.rect.right < -5 or self.rect.top > SCREEN_HEIGHT + 5:     
            self.spawn_new_enemy()

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x +=self.speed_x
        self.boundary()

    def move(self):
        global SCORE
        
        self.rect.move_ip(0,self.speed_y)
        if (self.rect.bottom > 1200):
            self.score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(90, 900), 0)