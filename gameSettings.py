from imports import *
#font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
#cursor
mouse_cursor_default = pygame.image.load("img\Cursors\cursor_default.png")
mouse_crusor_hover = pygame.image.load("img\Cursors\cursor_select.png")
pygame.mouse.set_visible(False)
#icon
icon = pygame.image.load("logo\logo32x32.png")
pygame.display.set_icon(icon)


#backgrounds and screen settings
background = pygame.image.load("img\Backgrounds\game_background_1.png").convert()
background_rect = background.get_rect
endAndBeginBackground = pygame.image.load("img\Backgrounds\BackgroundEnd.jpg").convert()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))




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


    
#functions
def reset_game():
    all_sprites.empty()
    all_enemies.empty()
    all_bullets.empty()
    player = Player(all_bullets, all_sprites)
    all_sprites.add(player)
    for i in range(9):
        spawn_new_enemy(all_enemies, all_sprites)

def change_volume(value):
    pygame.mixer.music.set_volume(value)


