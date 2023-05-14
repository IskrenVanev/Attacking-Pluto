import pygame
import sys
from enemy import Enemy
import random, time
from os import path


BLACK = (0, 0, 0)
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

def spawn_new_enemy(all_enemies, all_sprites):
    e = Enemy()
    all_enemies.add(e)
    all_sprites.add(e)




