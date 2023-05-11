import pygame
import sys
from pygame.locals import *
import random, time
from player import Player
from enemy import Enemy
from bullet import Bullet
from os import path
from game_functions import *


#settings
pygame.init()
icon = pygame.image.load("logo\logo32x32.png")
pygame.display.set_icon(icon)
FPS = 140
clock = pygame.time.Clock()
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")
background = pygame.image.load("img\Free-Horizontal-Game-Backgrounds\PNG\game_background_1\game_background_1.png").convert()
background_rect = background.get_rect
#FramePerSec = pygame.time.Clock()


# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over!", True, BLACK)

#SPEED_Y = 5
#SCORE = 0



#background = pygame.image.load("img\Free-Horizontal-Game-Backgrounds\PNG\game_background_1\game_background_1.png")



pygame.display.set_caption("Attacking Uranus")





#All sprites


all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
player = Player(all_bullets, all_sprites)
all_sprites.add(player)

for i in range(9):
    spawn_new_enemy(all_enemies, all_sprites)
     




running = True
while running:
    #keep the game running at 140 fps
    clock.tick(FPS)
    #Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
        
    #Update: 
    all_sprites.update()
 
    #check if enemy hits the ship 
    enemy_collision = pygame.sprite.spritecollide(player, all_enemies, False)
    if enemy_collision:
        running = False

    #check to see if a bullet hits enemy
    bullet_collision = pygame.sprite.groupcollide(all_enemies, all_bullets, True, True)
    for collision in bullet_collision:
        spawn_new_enemy(all_enemies, all_sprites)
        
    #Draw to the screen
    screen.blit(background, (0,0))
    all_sprites.draw(screen)

    #Update after drawing evertything to the screen:
    pygame.display.update()

pygame.quit()



    #     if event.type == INC_SPEED:
    #         for enemy in enemies:
    #             enemy.speed_y += random.uniform(0.1, 0.5)
    #     if event.type == INC_SPEED_X:   
    #         for enemy in enemies:
    #             enemy.speed_x += random.uniform(0.1, 0.5)      
        

    # screen.blit(background, (0,0))
    # thescore = 0
    # for enemy in enemies:
    #     thescore += enemy.score 
    # scores = font_small.render(str(thescore), True, BLACK)
    # screen.blit(scores, (10,10))
    # #Moves and Re-draws all Sprites
    # for entity in all_sprites:
    #     entity.move()
    #     screen.blit(entity.image, entity.rect)
        

    # #To be run if collision occurs between Player and Enemy
    # if pygame.sprite.spritecollideany(P1, enemies):
    #     pygame.mixer.Sound('sounds\ExplosionGGWP.wav').play()
    #     time.sleep(1) FramePerSec
    #     screen.fill(RED)
    #     screen.blit(game_over, (SCREEN_WIDTH/2 - game_over.get_width()/2, SCREEN_HEIGHT/2 - game_over.get_height()/2))
    #     pygame.display.update()
    #     for entity in all_sprites:
    #         entity.kill()
    #     time.sleep(2)
    #     pygame.quit()
    #     sys.exit()

    # pygame.display.update()
    # FramePerSec.tick(FPS)