from imports import *
from gameSettings import *
from pygame import mixer
from pygame.sprite import Sprite
from enemyLvl2 import Enemy2
# Settings
pygame.init()
pygame.mixer.init()
mixer.music.load('sounds/Background_song.mp3')
mixer.music.set_volume(0.0)
mixer.music.play(-1)
FPS = 140
clock = pygame.time.Clock()
explosion_sound_channel = pygame.mixer.Channel(1)
lvlUpSound = pygame.mixer.Channel(2)
lvlUpSound.set_volume(0.2)
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
def spawn_new_enemy2(all_enemies, all_sprites):
    e = Enemy2(alien_bullet_group, all_sprites)
    all_enemies.add(e)
    all_sprites.add(e)

#best_score = 0
try:
    with open('best_score.txt', 'r') as file:
        content = file.read()
        if content:
            best_score = int(content)
        else:
            best_score = 0  # or any other default value
except FileNotFoundError:
    best_score = 0  # Handle the case when the file doesn't exist



 
def play():
    global best_score
    global background_y
    global collision_sound_played
    lvl2wp = pygame.image.load("img\Backgrounds\Lvl2WP.jpg")
    global explosion_sound_played
    game_over_flag = False
    running = True
    player = Player(all_bullets, all_sprites)
    all_sprites.add(player)
    collision_sound_played = False  # Initialize collision_sound_played
    start_time = pygame.time.get_ticks()
    enemyCollide = False
    pausetime = 140
    collision_enemies = []
    hasCollided = False
    collisionCounter = 0
    
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
            if hasCollided == False:
                hasCollided = True
            for enemy in all_enemies:
                if hasCollided == True and collisionCounter % 7 != 0:
                    Enemy.collide_with_player(enemy)
                    collisionCounter+=1
                if collisionCounter % 7 == 0:
                    hasCollided=False
            
                
            
            player.explode()
            player.lives -= 1
          

            if player.lives >=1:        #empty sprites and spawn them again
                all_sprites.empty()
                all_enemies.empty()
                all_bullets.empty()
                all_sprites.add(player)
                player.rect.bottom = SCREEN_HEIGHT - 10
                for i in range(7):
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
        if bullet_collision:
            for enemy_sprite, bullet_sprites in bullet_collision.items():
        # Check the enemy images and assign scores accordingly
                enemy_images = enemy_sprite.enemy_images     
                if any(image_path in enemy_images for image_path in Enemy.enemy_bat_images):
                    Enemy.SCORE += 1  # Score for shooting enemy_bat_images
                elif any(image_path in enemy_images for image_path in Enemy.enemy_eye_images):
                    Enemy.SCORE += 2  # Score for shooting enemy_eye_images
                elif any(image_path in enemy_images for image_path in Enemy.enemy_dragon_images):
                    Enemy.SCORE += 3  # Score for shooting enemy_dragon_images
                
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
        
            
        if not enemyCollide:
            enemyCollide = False
        all_sprites.draw(screen)
        
        
            
        
        for collision in bullet_collision: 
            enemy = collision
            enemy_x = enemy.rect.x
            enemy_y = enemy.rect.y
            show_explosion_animation(enemy_x, enemy_y)
            spawn_new_enemy(all_enemies, all_sprites)
            explosion_sound_channel.play(pygame.mixer.Sound('img/Explosions/ExplosionSound1.wav'))
        
            
        pygame.display.update()
        

       
        
        if Enemy.SCORE > best_score:
                best_score = Enemy.SCORE
                with open('best_score.txt', 'w') as file:
                    file.write(str(best_score))
        if Enemy.SCORE >= 20:
            break
            
    if Enemy.SCORE >= 20:
        screen.blit(lvl2wp, (0, 0))
        level_text = font.render("Level 2", True, RED)
        text_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(level_text, text_rect)
        all_sprites.empty()
        all_enemies.empty()
        all_bullets.empty()
        pygame.display.update()
        lvlUpSound.play(pygame.mixer.Sound("sounds/LVLUPSOUND.mp3"))
        pygame.time.wait(2000)
        game_over_flag = False
        collision_sound_played = False
        play2()            
    game_over_flag = False
    collision_sound_played = False
    death_menu()
    







#TODO: Make level 2
def play2():
    #print("entered level 2")
    lvl2wp = pygame.image.load("img\Backgrounds\Lvl2WP.jpg")
    global best_score
    global background_y
    firstLoop= False
    firstLoopCnt = 0
    global collision_sound_played
    global explosion_sound_played
    game_over_flag = False
    running = True
    player = Player(all_bullets, all_sprites)
    all_sprites.add(player)
    collision_sound_played = False  # Initialize collision_sound_played
    start_time = pygame.time.get_ticks()
    enemyCollide = False
    pausetime = 140
    collision_enemies = []
    hasCollided = False
    collisionCounter = 0
    for i in range(4):  
        spawn_new_enemy2(all_enemies, all_sprites)
    while running:
        
        clock.tick(FPS)
        firstLoopCnt+=1
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        screen.fill((0, 0, 0))

        if not game_over_flag:
            #might need to update alien bullets!
            
            all_sprites.update()
 # Enemy collision
        enemy_collision = pygame.sprite.spritecollide(player, all_enemies, False)
        if enemy_collision:
            if hasCollided == False:
                hasCollided = True
            for enemy in all_enemies:
                if hasCollided == True and collisionCounter % 7 != 0:
                    Enemy.collide_with_player(enemy)
                    collisionCounter+=1
                if collisionCounter % 7 == 0:
                    hasCollided=False
 
            player.explode()
            player.lives -= 1
          

            if player.lives >=1:        #empty sprites and spawn them again
                all_sprites.empty()
                all_enemies.empty()
                all_bullets.empty()
                alien_bullet_group.empty()
                all_sprites.add(player)
                player.rect.bottom = SCREEN_HEIGHT - 10
                for i in range(4):
                    spawn_new_enemy2(all_enemies, all_sprites)
            
            if not collision_sound_played:      #play explosion
                explosion_sound_channel.play(pygame.mixer.Sound('sounds/ExplosionGGWP.wav'))
                collision_sound_played = True
                
            collision_sound_played = False
            if player.lives <= 0: #ggwp
                Enemy.SCORE = 0
                break
# Getting the collision coordinates for bullets
        bullet_collision = pygame.sprite.groupcollide(all_enemies, all_bullets, True, True)
        if bullet_collision:
            for enemy_sprite, bullet_sprites in bullet_collision.items():
        # Check the enemy images and assign scores accordingly
                enemy_images = enemy_sprite.enemy_images     
                if any(image_path in enemy_images for image_path in Enemy2.enemy_alien_spaceship_ver1):
                    Enemy.SCORE += 1  # Score for shooting enemy_bat_images
                elif any(image_path in enemy_images for image_path in Enemy2.enemy_alien_spaceship_ver2):
                    Enemy.SCORE += 2  # Score for shooting enemy_eye_images
               


        bullet_collision2 = pygame.sprite.spritecollide(player, alien_bullet_group, False)
        if bullet_collision2:
            for bullet in alien_bullet_group:
                bullet.kill()
            if hasCollided == False:
                hasCollided = True
            for enemy in all_enemies:
                if hasCollided == True and collisionCounter % 7 != 0:
                    Enemy.collide_with_player(enemy)
                    collisionCounter+=1
                if collisionCounter % 7 == 0:
                    hasCollided=False
            player.explode()
            player.lives -= 1        

            if player.lives >=1:        #empty sprites and spawn them again
                all_sprites.empty()
                all_enemies.empty()
                all_bullets.empty()
                all_sprites.add(player)
                player.rect.bottom = SCREEN_HEIGHT - 10
                for i in range(4):
                    spawn_new_enemy2(all_enemies, all_sprites)
            
            if not collision_sound_played:      #play explosion
                explosion_sound_channel.play(pygame.mixer.Sound('sounds/ExplosionGGWP.wav'))
                collision_sound_played = True
                
            collision_sound_played = False
            if player.lives <= 0: #ggwp
                Enemy.SCORE = 0
                break



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
        if Enemy.SCORE>= 20 and firstLoop == 1:
            Enemy2.SCORE = Enemy.SCORE + Enemy2.SCORE
        scores = font_average.render(str(Enemy2.SCORE+Enemy.SCORE), True, WHITE)
        
        player.draw_hearts(screen)
        
        screen.blit(scores, (10, 10))
        
            
        if not enemyCollide:
            enemyCollide = False
        all_sprites.draw(screen)
        
        
            
        
        for collision in bullet_collision: 
            enemy = collision
            enemy_x = enemy.rect.x
            enemy_y = enemy.rect.y
            show_explosion_animation(enemy_x, enemy_y)
            spawn_new_enemy2(all_enemies, all_sprites)
            explosion_sound_channel.play(pygame.mixer.Sound('img/Explosions/ExplosionSound1.wav'))
        
            
        pygame.display.update()
        
        
       
        
        if Enemy.SCORE + Enemy2.SCORE > best_score:
                best_score = Enemy.SCORE + Enemy2.SCORE
                with open('best_score.txt', 'w') as file:
                    file.write(str(best_score))  
        if Enemy.SCORE  + Enemy2.SCORE>= 40:
            break 
    if Enemy.SCORE  + Enemy2.SCORE>= 40:
        screen.blit(lvl2wp, (0, 0))
        level_text = font.render("Level 3", True, RED)
        text_rect = level_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(level_text, text_rect)
        all_sprites.empty()
        all_enemies.empty()
        all_bullets.empty()
        alien_bullet_group.empty()
        pygame.display.update()
        lvlUpSound.play(pygame.mixer.Sound("sounds/LVLUPSOUND.mp3"))
        pygame.time.wait(2000)
        game_over_flag = False
        collision_sound_played = False
        play3()                     
    game_over_flag = False
    collision_sound_played = False
    death_menu()
    


def play3():
    #print("entered level 2")
    lvl2wp = pygame.image.load("img\Backgrounds\Lvl2WP.jpg")
    global best_score
    global background_y
    global collision_sound_played
    global explosion_sound_played
    game_over_flag = False
    running = True
    player = Player(all_bullets, all_sprites)
    all_sprites.add(player)
    collision_sound_played = False  # Initialize collision_sound_played
    start_time = pygame.time.get_ticks()
    enemyCollide = False
    pausetime = 140
    collision_enemies = []
    hasCollided = False
    collisionCounter = 0
    #for i in range(4):  
     #   spawn_new_enemy(all_enemies, all_sprites)
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
            if hasCollided == False:
                hasCollided = True
            for enemy in all_enemies:
                if hasCollided == True and collisionCounter % 7 != 0:
                    Enemy.collide_with_player(enemy)
                    collisionCounter+=1
                if collisionCounter % 7 == 0:
                    hasCollided=False
 
            player.explode()
            player.lives -= 1
          

            if player.lives >=1:        #empty sprites and spawn them again
                all_sprites.empty()
                all_enemies.empty()
                all_bullets.empty()
                all_sprites.add(player)
                player.rect.bottom = SCREEN_HEIGHT - 10
                for i in range(7):
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
        if bullet_collision:
            for enemy_sprite, bullet_sprites in bullet_collision.items():
        # Check the enemy images and assign scores accordingly
                enemy_images = enemy_sprite.enemy_images     
                if any(image_path in enemy_images for image_path in Enemy.enemy_bat_images):
                    Enemy.SCORE += 1  # Score for shooting enemy_bat_images
                elif any(image_path in enemy_images for image_path in Enemy.enemy_eye_images):
                    Enemy.SCORE += 2  # Score for shooting enemy_eye_images
                elif any(image_path in enemy_images for image_path in Enemy.enemy_dragon_images):
                    Enemy.SCORE += 3  # Score for shooting enemy_dragon_images
                
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
        scores = font_average.render(str(Enemy.SCORE + Enemy2.SCORE), True, WHITE)
        
        player.draw_hearts(screen)
        
        screen.blit(scores, (10, 10))
        
            
        if not enemyCollide:
            enemyCollide = False
        all_sprites.draw(screen)
        
        
            
        
        for collision in bullet_collision: 
            enemy = collision
            enemy_x = enemy.rect.x
            enemy_y = enemy.rect.y
            show_explosion_animation(enemy_x, enemy_y)
            spawn_new_enemy(all_enemies, all_sprites)
            explosion_sound_channel.play(pygame.mixer.Sound('img/Explosions/ExplosionSound1.wav'))
        
            
        pygame.display.update()
        

       
        
        if Enemy.SCORE > best_score:
                best_score = Enemy.SCORE
                with open('best_score.txt', 'w') as file:
                    file.write(str(best_score))  
        
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


        best_score_text = font_average.render(f"Best Score: {best_score}", True, WHITE)
        screen.blit(best_score_text, (10, 10))



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



