from imports import *
from gameSettings import *
from pygame import mixer
#settings
pygame.init()
pygame.mixer.init()
mixer.music.load('sounds\Background_song.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)
FPS = 140
clock = pygame.time.Clock()
explosion_sound_channel = pygame.mixer.Channel(1)
explosion_sound_channel.set_volume(0.2)
font = pygame.font.SysFont("Verdana", 100)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over!", True, WHITE)
endBackground = pygame.image.load("img\Backgrounds\BackgroundEnd.jpg").convert()


running = True
game_over_flag = False
collision_sound_played = False


def play():
    game_over_flag = False
    running = True
    player = Player(all_bullets, all_sprites)
    all_sprites.add(player)
    
    collision_sound_played = False  # Initialize collision_sound_played
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
         
        if not game_over_flag:
            all_sprites.update()

        enemy_collision = pygame.sprite.spritecollide(player, all_enemies, False)
        if enemy_collision:
            if not collision_sound_played:
                explosion_sound_channel.play(pygame.mixer.Sound('sounds\ExplosionGGWP.wav'))
                collision_sound_played = True           
            break

        bullet_collision = pygame.sprite.groupcollide(all_enemies, all_bullets, True, True)
        for collision in bullet_collision:
            spawn_new_enemy(all_enemies, all_sprites)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.update()
    game_over_flag = False
    collision_sound_played = False
    death_menu()
   

    
def options():
    while True:
        SCREEN.blit(endAndBeginBackground, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

       

        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 150))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = buttons.Button(image=None, pos=(SCREEN_WIDTH // 2 , 1000), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        


        VOLUME_TEXT = get_font(40).render("CHANGE MUSIC VOLUME", True, WHITE)
        VOLUME_RECT = VOLUME_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 300))
        SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)

        VOLUME_EFFECTS_TEXT = get_font(40).render("CHANGE EFFECTS VOLUME", True, WHITE)
        VOLUME_EFFECTS_RECT = VOLUME_EFFECTS_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 600))
        SCREEN.blit(VOLUME_EFFECTS_TEXT, VOLUME_EFFECTS_RECT)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        VOLUME_BAR_WIDTH = 700
        VOLUME_BAR_HEIGHT = 100
        VOLUME_BAR_X = SCREEN_WIDTH // 2 - VOLUME_BAR_WIDTH // 2
        VOLUME_BAR_Y = 400
        VOLUME_BAR_BORDER_WIDTH = 2

        VOLUME_BAR_SFX_WIDTH = 700
        VOLUME_BAR_SFX_HEIGHT = 100
        VOLUME_BAR_SFX_X = SCREEN_WIDTH // 2 - VOLUME_BAR_SFX_WIDTH // 2
        VOLUME_BAR_SFX_Y = 700
        VOLUME_BAR_SFX_BORDER_WIDTH = 2

        # Calculate the current volume position on the bar
        volume_position = pygame.mixer.music.get_volume() * (VOLUME_BAR_WIDTH - VOLUME_BAR_BORDER_WIDTH)
        sfx_volume_position = explosion_sound_channel.get_volume() * (VOLUME_BAR_SFX_WIDTH - VOLUME_BAR_SFX_BORDER_WIDTH)

        # Draw the volume bar
        pygame.draw.rect(SCREEN, (255, 255, 255), (VOLUME_BAR_X, VOLUME_BAR_Y, VOLUME_BAR_WIDTH, VOLUME_BAR_HEIGHT), 0)
        pygame.draw.rect(SCREEN, (0, 0, 0), (VOLUME_BAR_X, VOLUME_BAR_Y, VOLUME_BAR_WIDTH, VOLUME_BAR_HEIGHT), VOLUME_BAR_BORDER_WIDTH)
        pygame.draw.rect(SCREEN, (255, 0, 0), (VOLUME_BAR_X, VOLUME_BAR_Y, volume_position, VOLUME_BAR_HEIGHT), 0)

        pygame.draw.rect(SCREEN, (255, 255, 255), (VOLUME_BAR_SFX_X, VOLUME_BAR_SFX_Y, VOLUME_BAR_SFX_WIDTH, VOLUME_BAR_SFX_HEIGHT), 0)
        pygame.draw.rect(SCREEN, (0, 0, 0), (VOLUME_BAR_SFX_X, VOLUME_BAR_SFX_Y, VOLUME_BAR_SFX_WIDTH, VOLUME_BAR_SFX_HEIGHT), VOLUME_BAR_SFX_BORDER_WIDTH)
        pygame.draw.rect(SCREEN, (255, 0, 0), (VOLUME_BAR_SFX_X, VOLUME_BAR_SFX_Y, sfx_volume_position, VOLUME_BAR_SFX_HEIGHT), 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            elif pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if VOLUME_BAR_X <= mouse_x <= VOLUME_BAR_X + VOLUME_BAR_WIDTH and VOLUME_BAR_Y <= mouse_y <= VOLUME_BAR_Y + VOLUME_BAR_HEIGHT:
                    # Calculate the new volume based on the mouse position
                    volume_position = mouse_x - VOLUME_BAR_X
                    volume = volume_position / (VOLUME_BAR_WIDTH - VOLUME_BAR_BORDER_WIDTH)
                    change_volume(volume)
                if VOLUME_BAR_SFX_X <= mouse_x <= VOLUME_BAR_SFX_X + VOLUME_BAR_SFX_WIDTH and VOLUME_BAR_SFX_Y <= mouse_y <= VOLUME_BAR_SFX_Y + VOLUME_BAR_SFX_HEIGHT:
                    # Calculate the new volume based on the mouse position
                    volume_position_sfx = mouse_x - VOLUME_BAR_SFX_X
                    volume = volume_position_sfx / (VOLUME_BAR_SFX_WIDTH - VOLUME_BAR_SFX_BORDER_WIDTH)
                    explosion_sound_channel.set_volume(volume)
        pygame.display.update()


def death_menu():
    while True:
        SCREEN.blit(endAndBeginBackground, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        DEATH_TEXT = get_font(100).render("YOU DIED!", True, "#b68f40")
        DEATH_RECT = DEATH_TEXT.get_rect(center=(960, 150))
        MAINMENU_BUTTON = buttons.Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(960, 400), 
                            text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        RETRY_BUTTON = buttons.Button(image=pygame.image.load("assets/Options Rect.png"), pos=(960, 600), 
                                text_input="RETRY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = buttons.Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(960, 800), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(DEATH_TEXT, DEATH_RECT)
        for button in [RETRY_BUTTON, QUIT_BUTTON,MAINMENU_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETRY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        reset_game()
                        play()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    if MAINMENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                        reset_game()
                        main_menu()
                    
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(endAndBeginBackground, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(960, 150))

        PLAY_BUTTON = buttons.Button(image=pygame.image.load("assets/Play Rect.png"), pos=(960, 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = buttons.Button(image=pygame.image.load("assets/Options Rect.png"), pos=(960, 600), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = buttons.Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(960, 800), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
               

        pygame.display.update()

main_menu()




