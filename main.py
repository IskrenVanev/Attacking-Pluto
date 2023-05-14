from imports import *
from gameSettings import *

#settings
pygame.init()
pygame.mixer.init()
FPS = 140
clock = pygame.time.Clock()
explosion_sound_channel = pygame.mixer.Channel(1)
font = pygame.font.SysFont("Verdana", 100)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over!", True, WHITE)


    


running = True
game_over_flag = False
collision_sound_played = False
explosion_sound_channel = pygame.mixer.Channel(1)




running = True
while running:
    #keep the game running at 140 fps
    clock.tick(FPS)
    #Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
        if event.type == MOUSEBUTTONDOWN:
             mouse_pos = pygame.mouse.get_pos()
             if quit_button.is_clicked(mouse_pos):
                 running=False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if retry_button.is_clicked(mouse_pos):
                # Reset game state here
                all_sprites.empty()
                all_enemies.empty()
                all_bullets.empty()
                player = Player(all_bullets, all_sprites)
                all_sprites.add(player)
                for i in range(9):
                    spawn_new_enemy(all_enemies, all_sprites)
                game_over_flag = False
                collision_sound_played = False
    
    if not game_over_flag:  
        #Update: 
        all_sprites.update()
 
    #check if enemy hits the ship 
        enemy_collision = pygame.sprite.spritecollide(player, all_enemies, False)
        if enemy_collision:
            if not collision_sound_played:
                explosion_sound_channel.play(pygame.mixer.Sound('sounds\ExplosionGGWP.wav'))
                collision_sound_played = True
            time.sleep(1)
            screen.blit(endBackground, (0,0))
            screen.blit(game_over, (SCREEN_WIDTH/2 - game_over.get_width()/2, SCREEN_HEIGHT/2 - game_over.get_height()/2))
            retry_button.draw(screen)
            quit_button.draw(screen)
            pygame.display.update()
            
            continue

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

