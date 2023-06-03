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
        self.explosion_images = [
            pygame.transform.scale(pygame.image.load("img/Explosions/Explosion3/Expl1.png"), (150, 150)),
            pygame.transform.scale(pygame.image.load("img/Explosions/Explosion3/Expl2.png"), (150, 150)),
            pygame.transform.scale(pygame.image.load("img/Explosions/Explosion3/Expl3.png"), (150, 150)),
            pygame.transform.scale(pygame.image.load("img/Explosions/Explosion3/Expl4.png"), (150, 150))
        ]
        self.heart_images =[
            pygame.image.load("img/Player/Hearts/Heart.png"),
            pygame.image.load("img/Player/Hearts/Noheart.png")
        ]

        self.original_image = pygame.image.load("img\Player\spaceship_black.png")
        self.original_image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * 0.2), int(self.original_image.get_height() * 0.2)))
        cropped_height = int(self.original_image.get_height() * 0.8)
        self.original_image = self.original_image.subsurface(pygame.Rect(0, 0, self.original_image.get_width(), cropped_height))
        self.rect = self.original_image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.bottom = SCREEN_HEIGHT-10
        self.image = self.original_image.copy()
        self.speed_x=0
        self.speed_y=0
        self.speed = 8
        self.all_bullets = all_bullets
        self.all_sprites = all_sprites
        self.last_bullet_shot = pygame.time.get_ticks()
        self.lives = 3

        self.is_exploding = False
        self.explosion_index = 0
        self.explosion_start_time = 0
        self.explosion_duration = 500  # milliseconds

    
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
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def movement(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speed_x = self.speed
        if keystate[pygame.K_LEFT]:
            self.speed_x = -self.speed    #8 pixels to the left
        if keystate[pygame.K_UP]:
            self.speed_y = -self.speed
        if keystate[pygame.K_DOWN]:
            self.speed_y = self.speed
        if keystate[pygame.K_SPACE]:
            self.shoot_bullet()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def draw_hearts(self, screen):
        heart_width = self.heart_images[0].get_width()
        heart_height = self.heart_images[0].get_height()
        heart_scale = 4  # Adjust the scale factor as needed

        heart_width *= heart_scale
        heart_height *= heart_scale

        for i in range(self.lives):
            heart_image = pygame.transform.scale(self.heart_images[0], (heart_width, heart_height))
            heart_x = SCREEN_WIDTH - (heart_width * (i + 1))
            heart_y = 0
            screen.blit(heart_image, (heart_x, heart_y))

        for i in range(self.lives, 3):
            noheart_image = pygame.transform.scale(self.heart_images[1], (heart_width, heart_height))
            noheart_x = SCREEN_WIDTH - (heart_width * (i + 1))
            noheart_y = 0
            screen.blit(noheart_image, (noheart_x, noheart_y))
    
    def explode(self):
        self.is_exploding = True
        self.explosion_start_time = pygame.time.get_ticks()
        self.explosion_index = 0
        #self.image = self.explosion_images[self.explosion_index]
        
    def update(self):
        if self.is_exploding:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.explosion_start_time

            if elapsed_time > self.explosion_duration:
                self.is_exploding = False
                self.image = self.original_image
                # Reset the player position or do any other necessary logic
            else:
                explosion_image = self.explosion_images[self.explosion_index]
                self.image = explosion_image
                self.explosion_index = (self.explosion_index + 1) % len(self.explosion_images)

        else:
            self.movement()
            self.boundary()
             