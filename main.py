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
endBackground = pygame.image.load("img\Backgrounds\BackgroundEnd.jpg").convert()


    


running = True
game_over_flag = False
collision_sound_played = False
explosion_sound_channel = pygame.mixer.Channel(1)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

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
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.is_clicked(mouse_pos):
                    running = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button.is_clicked(mouse_pos):
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
            all_sprites.update()

        enemy_collision = pygame.sprite.spritecollide(player, all_enemies, False)
        if enemy_collision:
            if not collision_sound_played:
                explosion_sound_channel.play(pygame.mixer.Sound('sounds\ExplosionGGWP.wav'))
                collision_sound_played = True
            time.sleep(1)
            screen.blit(endBackground, (0, 0))
            screen.blit(game_over, (SCREEN_WIDTH / 2 - game_over.get_width() / 2, SCREEN_HEIGHT / 2 - game_over.get_height() / 2))
            retry_button.draw(screen)
            quit_button.draw(screen)
            pygame.display.update()
            continue
            running = False

        bullet_collision = pygame.sprite.groupcollide(all_enemies, all_bullets, True, True)
        for collision in bullet_collision:
            spawn_new_enemy(all_enemies, all_sprites)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.update()

    pygame.quit()

    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(960, 440))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = buttons.Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(endAndBeginBackground, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(960, 150))

        PLAY_BUTTON = buttons.Button(image=pygame.image.load("assets/Play Rect.png"), pos=(960, 440), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = buttons.Button(image=pygame.image.load("assets/Options Rect.png"), pos=(960, 600), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = buttons.Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(960, 760), 
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




