from imports import *
#from explosion import Explosion
from enemy import Enemy
FPS = 60
clock = pygame.time.Clock()
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
pygame.display.set_caption("Attacking Pluto")



#All sprites
all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
#player_group = pygame.sprite.Group()
#all_explosions = pygame.sprite.Group()
player = Player(all_bullets, all_sprites)
all_sprites.add(player)
#player_group.add(player)
#explosion = Explosion(Enemy.rect.centerx, enemy.rect.centery)
#all_explosions.add(explosion)

for i in range(7):  
    spawn_new_enemy(all_enemies, all_sprites)


    
#functions
def reset_game():
    all_sprites.empty()
    all_enemies.empty()
    all_bullets.empty()
    player = Player(all_bullets, all_sprites)
    all_sprites.add(player)
    for i in range(7):
        spawn_new_enemy(all_enemies, all_sprites)
    Enemy.SCORE=0

def change_volume(value):
    pygame.mixer.music.set_volume(value)



#explosions

explosion_images = []
explosion_images.append(pygame.image.load("img\Explosions\Explosion1.png"))
explosion_images.append(pygame.image.load("img\Explosions\Explosion2.png"))
explosion_images.append(pygame.image.load("img\Explosions\Explosion3.png"))
explosion_images.append(pygame.image.load("img\Explosions\Explosion4.png"))


def show_explosion_animation(x, y):
    explosion_duration = 200  # Duration in milliseconds
    frame_delay = explosion_duration // len(explosion_images)
    current_frame = 0
    animation_timer = 0
    
    while animation_timer < explosion_duration:
        clock.tick(FPS)
        animation_timer += frame_delay
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(explosion_images[current_frame], (x, y))
        pygame.display.update()
        
        current_frame += 1
        if current_frame >= len(explosion_images):
            current_frame = 0