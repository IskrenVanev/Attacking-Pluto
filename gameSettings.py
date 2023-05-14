from imports import *


#icon
icon = pygame.image.load("logo\logo32x32.png")
pygame.display.set_icon(icon)


#backgrounds and screen settings
background = pygame.image.load("img\Backgrounds\game_background_1.png").convert()
background_rect = background.get_rect
endBackground = pygame.image.load("img\Backgrounds\BackgroundEnd.jpg").convert()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#name of the game
pygame.display.set_caption("Attacking Uranus")



#All sprites
all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
player = Player(all_bullets, all_sprites)
all_sprites.add(player)

for i in range(9):  
    spawn_new_enemy(all_enemies, all_sprites)


    

#buttons
retry_button = buttons.RetryButton(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200)
quit_button = buttons.QuitButton(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 200, 200, 100)