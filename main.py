from imports import *
from gameSettings import *
from pygame import mixer
from pygame.sprite import Sprite

# Settings
pygame.init()
pygame.mixer.init()
mixer.music.load('sounds/Background_song.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)
FPS = 140
clock = pygame.time.Clock()
explosion_sound_channel = pygame.mixer.Channel(1)
explosion_sound_channel.set_volume(0.2)
font = pygame.font.SysFont("Verdana", 100)
font_average = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over!", True, WHITE)
endBackground = pygame.image.load("img/Backgrounds/BackgroundEnd.jpg").convert()
bg_image = pygame.image.load("img/Backgrounds/Dynamic Space Background FREE/img1.png").convert()
bg_image2 = pygame.image.load("img/Backgrounds/Dynamic Space Background FREE/img2.png").convert()
bg_image3 = pygame.image.load("img/Backgrounds/Dynamic Space Background FREE/img3.png").convert()
background_height = bg_image.get_height()
background_y = 0  # Initial y-position of the background
running = True
game_over_flag = False
collision_sound_played = False
explosion_player_image = pygame.image.load("img\Explosions\Explosion3\Expl1.png")
explosion_frames = [
    pygame.image.load("img/Explosions/Explosion3/Expl1.png"),
    pygame.image.load("img/Explosions/Explosion3/Expl2.png"),
    pygame.image.load("img/Explosions/Explosion3/Expl3.png"),
    pygame.image.load("img/Explosions/Explosion3/Expl4.png")
    

]



 
def play():
    global background_y
    global collision_sound_played
    global explosion_sound_played
    game_over_flag = False
    running = True
    player = Player(all_bullets, all_sprites)
    all_sprites.add(player)
    collision_sound_played = False  # Initialize collision_sound_played
    start_time = pygame.time.get_ticks()
    #delay = 200  # Delay in milliseconds (1 second)
    #explosion_active = False
    freeze_screen = False
    explosion_active = False  # Flag to track the explosion state
    current_frame = 0  # Current frame index
    frame_start_time = 0  # Start time for the current frame
    frame_duration = 100  # Duration (in milliseconds) for each frame
    explosion_duration = 500
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        screen.fill((0, 0, 0))
        if not game_over_flag:
            all_sprites.update()
         
        
        # Enemy collision
        enemy_collision = pygame.sprite.spritecollide(player, all_enemies, False)
        if enemy_collision:
           
            player.lives -= 1
            if player.lives >=1:        #empty sprites and spawn them again
                all_sprites.empty()
                all_enemies.empty()
                all_bullets.empty()
                all_sprites.add(player)
                for i in range(9):
                    spawn_new_enemy(all_enemies, all_sprites)
            
            if not collision_sound_played:      #play explosion
                explosion_sound_channel.play(pygame.mixer.Sound('sounds/ExplosionGGWP.wav'))
                collision_sound_played = True
            collision_sound_played = False
            if player.lives <= 0: #ggwp
                Enemy.SCORE = 0
                break

        # Getting the collision coordinates for bullets
        bullet_collision = pygame.sprite.groupcollide(all_enemies, all_bullets, True, True)
        collision_coordinates = []
        for enemy_sprite, bullet_sprites in bullet_collision.items():
            for bullet_sprite in bullet_sprites:
                bullet_coordinates = (bullet_sprite.rect.x, bullet_sprite.rect.y)
                collision_coordinates.append(bullet_coordinates)


        # Scrolling background
        background_y = (background_y + 3) % background_height
        # Draw the background on the screen
        if player.lives == 3:
            screen.blit(bg_image, (0, background_y))
            screen.blit(bg_image, (0, background_y - background_height))
        elif player.lives == 2:
            screen.blit(bg_image2, (0, background_y))
            screen.blit(bg_image2, (0, background_y - background_height))
        elif player.lives == 1:
            screen.blit(bg_image3, (0, background_y))
            screen.blit(bg_image3, (0, background_y - background_height))
        scores = font_average.render(str(Enemy.SCORE), True, WHITE)
        player.draw_hearts(screen)
        
        screen.blit(scores, (10, 10))
        

        all_sprites.draw(screen)
        
        
            
        
        for collision in bullet_collision: 
            enemy = collision
            enemy_x = enemy.rect.x
            enemy_y = enemy.rect.y
            show_explosion_animation(enemy_x, enemy_y)
            spawn_new_enemy(all_enemies, all_sprites)
            explosion_sound_channel.play(pygame.mixer.Sound('img/Explosions/ExplosionSound1.wav'))
        
            
        pygame.display.update()
        current_time = pygame.time.get_ticks()

        if enemy_collision:  # Check if collision with enemy has occurred
            player.image = explosion_frames[current_frame]
            player.image = pygame.transform.scale(player.image, (300, 300))
            player.rect.bottom = SCREEN_HEIGHT - 60
            explosion_active = True  # Set the explosion flag to activate the animation
            frame_start_time = pygame.time.get_ticks()  # Record the start time of the current frame
            freeze_screen = True

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - frame_start_time

        if explosion_active:
            if elapsed_time >= frame_duration:  # Check if the current frame duration has passed
                current_frame += 1  # Move to the next frame
                if current_frame >= len(explosion_frames):  # Check if all frames have been displayed
                   
                    #pygame.time.delay(500)
                    
                    if elapsed_time >= explosion_duration:  # Check if the entire explosion duration has passed
                        explosion_active = False  # Deactivate the explosion animation
                        current_frame = 0  # Reset the frame index
                        pygame.time.delay(500)  # Delay after the explosion animation
                        # ... (reset the game state as needed)
                        
                        # Reset the player image
                        player.image = pygame.image.load("img/Player/spaceship_black.png")
                        player.image = pygame.transform.scale(player.image, (int(player.image.get_width() * 0.2), int(player.image.get_height() * 0.2)))
                        player.rect.centerx = SCREEN_WIDTH/2
                        player.rect.bottom = SCREEN_HEIGHT - 10
                        # ... (reset the game state as needed)
                    else:
                        current_frame = len(explosion_frames) - 1  # Show the last frame continuously
                    player.image = pygame.image.load("img/Player/spaceship_black.png")
                    player.image = pygame.transform.scale(player.image, (int(player.image.get_width() * 0.2), int(player.image.get_height() * 0.2)))
                    player.rect.bottom = SCREEN_HEIGHT - 10
                    explosion_active = False
                    frame_start_time = pygame.time.get_ticks()  # Record the start time of the next frame
                else:
                    player.image = explosion_frames[current_frame]  # Update the player image with the next frame
                    player.image = pygame.transform.scale(player.image, (300, 300))
                    frame_start_time = pygame.time.get_ticks()  # Record the start time of the next frame
                    
        
                
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
        #screen.blit(mouse_cursor_default, OPTIONS_MOUSE_POS)
        button_hovered = False
        for button in [OPTIONS_BACK]:
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)
            if button.rect.collidepoint(OPTIONS_MOUSE_POS):
                    screen.blit(mouse_crusor_hover, OPTIONS_MOUSE_POS)
                    button_hovered = True
        if not button_hovered:
            SCREEN.blit(mouse_cursor_default, OPTIONS_MOUSE_POS)
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
        button_hovered = False
        for button in [RETRY_BUTTON, QUIT_BUTTON,MAINMENU_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
                if button.rect.collidepoint(MENU_MOUSE_POS):
                    screen.blit(mouse_crusor_hover, MENU_MOUSE_POS)
                    button_hovered = True
                
                    
        if not button_hovered:
            SCREEN.blit(mouse_cursor_default, MENU_MOUSE_POS)
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
        button_hovered = False
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            if button.rect.collidepoint(MENU_MOUSE_POS):
                    screen.blit(mouse_crusor_hover, MENU_MOUSE_POS)
                    button_hovered = True
        if not button_hovered:
            SCREEN.blit(mouse_cursor_default, MENU_MOUSE_POS)
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



