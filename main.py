# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# X account : @ScissorMarks
# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0
# Spike sprites by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters
# Graphic images : "Pixel Adventure"
# https://pixelfrog-assets.itch.io/pixel-adventure-1

# main.py
# imports
import pygame
import math
from constants import WIDTH, HEIGHT, DARK_GREY, MUSTARD, WHITE, LIGHT_GRAY, FPS
from player import Player
from sounds import load_sounds
from images import coin_frames, coin_image, enemy_image, heart_image_16,heart_image_32, lives_image, title_image
from init_game import init
from collectibles.coin_collectible import Coin
from collectibles.life_collectible import Life
from collectibles.heart_collectible import Heart
from utils import drawText
from level_loader import load_level, load_level_tmx
from levels.level_0 import get_debug_platforms, get_debug_coins, get_debug_lives, get_debug_hearts, get_debug_enemies
from levels.level_1 import get_platforms as get_tmx_platforms
from camera import Camera

# init
screen, clock, font = init()

# global variables
score = 0
lives = 3
hearts = 3
coins_for_life = 0
sound_played = False
win_time = 0
life_lost_time = 0
last_hit_time = 0
transition_timer = 0

# game states = home // main_menu // transition_to_play // playing // win // lose
game_state = 'home'
is_debug = False
menu_selection = 0

# sounds
sounds = load_sounds()
sounds["game_over"].set_volume(0.33)
sounds["home_select"].set_volume(0.5)

# tiles
tiles = []

# player
player = Player()

# platforms
platforms = []

# coins
coins = []

# enemies
enemies = []

# life collectibles
life_collectibles = []

# heart collectibles
hearts_collectibles = []

# camera
camera = None

running = True
while running:
# game loop

    # -----
    # INPUT
    # -----

     # player input
    keys = pygame.key.get_pressed() # Held (maintenues) keys (True/False)

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # when space is pressed on the home screen, go to the main menu
        if game_state == "home" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sounds["home_select"].play()
                game_state = "main_menu"

        # handle navigation in the main menu
        if game_state == "main_menu":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    menu_selection = (menu_selection - 1) % 2
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    menu_selection = (menu_selection + 1) % 2
                if event.key == pygame.K_RETURN:
                    if menu_selection == 0:
                        # load tmx level
                        is_debug = False
                        from level_loader import load_level
                        platforms, coins, enemies, life_collectibles, hearts_collectibles, tiles = load_level("levels/tmx/level_1.tmx", coin_frames, lives_image, heart_image_16)
                        camera = Camera(player, 4000, 512, WIDTH, HEIGHT)
                        coins = []
                        enemies = []
                        life_collectibles = []
                        hearts_collectibles = []
                        game_state = "transition_to_play"
                        transition_timer = pygame.time.get_ticks()
                    elif menu_selection == 1:
                        # debug mode
                        is_debug = True
                        platforms = get_debug_platforms()
                        coins = get_debug_coins(coin_frames)
                        enemies = get_debug_enemies()
                        life_collectibles = get_debug_lives(lives_image)
                        hearts_collectibles = get_debug_hearts(heart_image_16)
                        tiles = []
                        camera = None
                        game_state = "transition_to_play"
                        transition_timer = pygame.time.get_ticks()

                
    # handle the transition screen
    if game_state == "transition_to_play":
        screen.fill(DARK_GREY)
        drawText(screen, font, "Get Ready...", WIDTH // 2, HEIGHT // 2, align="center")
        if pygame.time.get_ticks() - transition_timer >= 1000:
                        game_state = "playing"

    # ------
    # UPDATE
    # ------

    # check if the game is in the "playing" state
    if game_state == "playing":
        dx = 0
        if player.state != "hurt":
            # move left
            if keys[pygame.K_LEFT]:
                dx = -4.2
                player.direction = "left"
                player.state = "walking"
            # move right
            elif keys[pygame.K_RIGHT]:
                dx = 4.2
                player.direction = "right"
                player.state = "walking"
            # if no horizontal movement keys are pressed
            else:
                player.state = "idle"
            # jump if the player is on the ground and presses space
            if keys[pygame.K_SPACE] and player.on_ground:
                player.jump()
                sounds["jump"].play()
        else:
            # apply knockback in the opposite direction if player == "hurt"
            dx = -0.6 if player.direction == "right" else 0.6

        # update
        player.update(platforms, dx=dx, dy=0)

        # if the player is falling
        if player.y > HEIGHT + 100:
            sounds["lose_life"].play()
            lives -= 1
            if lives <= 0:
                game_state = "lose"
            else:
                hearts = 3
                game_state = "life_lost"
                life_lost_time = pygame.time.get_ticks()
            continue

        # check for collisions between the player and coins
        for coin in coins[:]:
            if player.get_rect().colliderect(coin.rect):
                coins.remove(coin)
                score += 1
                coins_for_life += 1
                sounds["coin"].play()
                # every 10 coins collected = gain 1 extra life (max 99 lives)
                if coins_for_life >= 10:
                    coins_for_life = 0
                    lives = min(lives + 1, 99)
                    hearts = 3
                    sounds["extra_life"].play()
        # check for collisions with lives (1-UP items)
        for life in life_collectibles[:]:
            if player.get_rect().colliderect(life.rect):
                life_collectibles.remove(life)
                lives = min(lives + 1, 99)  # add one life (max 99)
                hearts = 3
                sounds["extra_life"].play()
        # check for collisions with hearts (healing items)
        for heart in hearts_collectibles[:]:
            if player.get_rect().colliderect(heart.rect):
                hearts_collectibles.remove(heart)
                hearts = min(hearts + 1, 3)  # add one heart (max 3)
                sounds["heart_pickup"].play()
        # check for collisions with enemies
        for enemy_rect in enemies[:]:
            if player.get_rect().colliderect(enemy_rect) and not player.is_invincible:
                if player.state != "hurt":
                    player.state = "hurt"
                    player.hurt_timer = pygame.time.get_ticks()
                    sounds["hit"].play()

                    if hearts > 1:
                        hearts -= 1 # lose one heart
                    else:
                        hearts = 0
                        lives -= 1 # lose one life
                        coins_for_life = 0
                        if lives <= 0:
                            game_state = "lose" # game over
                        else:
                            hearts = 3
                            sounds["lose_life"].play()
                            game_state = "life_lost"
                            life_lost_time = pygame.time.get_ticks()
                break

        # update camera position
        if camera:
            camera.update()
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(DARK_GREY)
        screen.blit(overlay, (0, 0))
     # ----
    # DRAW
    # ----
    # background
    
    if game_state == "home":
        screen.fill(DARK_GREY)

        # draw
        title_x = (WIDTH - title_image.get_width()) // 2
        title_y = HEIGHT // 4 - 50

        screen.blit(title_image, (title_x, title_y))
        # make the "Press SPACE to Start" text blink
        if (pygame.time.get_ticks() // 420) % 2 == 0:
            drawText(screen, font, "Press SPACE to Start", WIDTH // 2, HEIGHT // 2 + 115, align="center")
        
    if game_state == "playing":
        # screen.fill(DARK_GREY)
        # platforms
        if tiles:
            for tile_img, pos in tiles:
                if camera:
                    draw_pos = camera.apply(pygame.Rect(pos[0], pos[1], tile_img.get_width(), tile_img.get_height()))
                    screen.blit(tile_img, draw_pos.topleft)
                else:
                    screen.blit(tile_img, pos)
        else:
            for plat in platforms:
                if camera:
                    draw_rect = camera.apply(plat)
                else:
                    draw_rect = plat
                pygame.draw.rect(screen, MUSTARD, draw_rect)
        # player
        player.draw(screen, camera)
        # coins
        for coin in coins:
            coin.draw(screen)
        # lives
        for life in life_collectibles:
            life.draw(screen)
        # enemies
        for enemy in enemies:
            screen.blit(enemy_image, (enemy.x, enemy.y))
        # hearts
        for heart in hearts_collectibles:
            heart.draw(screen)

        # player informations
        # lives icon with count
        icon_x = 10
        icon_y = 10

        # draw the player face icon (number of lives)
        screen.blit(lives_image, (icon_x, icon_y))

        # align text with icon
        text_y = icon_y + (lives_image.get_height() - font.get_height()) // 2

        # draw "x"
        x_surface = font.render("x", True, WHITE)
        x_x = icon_x + lives_image.get_width() + 10  # 2px after the icon
        screen.blit(x_surface, (x_x, text_y))

        # number of lives
        lives_surface = font.render(str(lives), True, WHITE)
        lives_x = x_x + x_surface.get_width() + 6  # 6px after the "x"
        screen.blit(lives_surface, (lives_x, text_y))

        # total width of "x" + "lives"
        text_total_width = lives_x + lives_surface.get_width() - icon_x

        # draw heart icons (for current health)
        for i in range(hearts):
            heart_x = icon_x + text_total_width + 15 + i * (heart_image_32.get_width() + 5)
            screen.blit(heart_image_32, (heart_x, icon_y))

        # score
        coin_rect = coin_image.get_rect()

        score_text = str(coins_for_life)
        score_width, _ = font.size(score_text)

        coin_x = WIDTH - coin_rect.width - 10
        coin_y = 10

        score_x = coin_x - 10
        score_y = 10

        # draw score and coin icon
        drawText(screen, font, score_text, score_x, score_y, WHITE, align="topright")
        screen.blit(coin_image, (coin_x, coin_y))

        # Only win automatically by collecting coins in debug mode
        if is_debug and len(coins) == 0:
            game_state = "win"
            win_time = pygame.time.get_ticks()
            sound_played = False

    if game_state == "win":
        screen.fill(DARK_GREY)
        
        if not sound_played and pygame.time.get_ticks() - win_time > 95:
            sounds["level_completed"].play()
            sound_played = True
        # settings
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(DARK_GREY)
        screen.blit(overlay, (0, 0))
        # draw win text
        drawText(screen, font, "YOU WIN!", WIDTH // 2, HEIGHT // 2, align="center")
    elif game_state == "main_menu":
        screen.fill(DARK_GREY)
        drawText(screen, font, "SELECT MODE", WIDTH // 2, HEIGHT // 4, align="center")

        options = ["Start Game", "Debug Level"]
        for i, option in enumerate(options):
            color = MUSTARD if i == menu_selection else LIGHT_GRAY
            drawText(screen, font, option, WIDTH // 2, HEIGHT // 2 + i * 40, color=color, align="center")
    elif game_state == "life_lost":
        # background color 
        screen.fill(DARK_GREY)

        # render the text surfaces first to know their sizes
        x_surface = font.render("x", True, MUSTARD)
        lives_surface = font.render(str(lives), True, MUSTARD)

        # total width = image width + padding + x width + padding + lives width
        total_width = lives_image.get_width() + 10 + x_surface.get_width() + 6 + lives_surface.get_width()

        # start x so that total is centered
        start_x = (screen.get_width() - total_width) // 2

        # total height = height of the lives image
        total_height = lives_image.get_height()

        # vertical start y to center the block vertically
        start_y = (screen.get_height() - total_height) // 2

        # position for the image
        icon_y = start_y

        # to center the text vertically (with the image)
        text_y = icon_y + (lives_image.get_height() - font.get_height()) // 2

        # draw the lives image
        screen.blit(lives_image, (start_x, icon_y))

        # calculate vertical center for the text
        text_y = icon_y + (lives_image.get_height() - font.get_height()) // 2

        x_surface = font.render("x", True, MUSTARD)
        x_x = start_x + lives_image.get_width() + 10
        screen.blit(x_surface, (x_x, text_y))

        lives_surface = font.render(str(lives), True, MUSTARD)
        lives_x = x_x + x_surface.get_width() + 6
        screen.blit(lives_surface, (lives_x, text_y))

        # 2 seconds timer
        if pygame.time.get_ticks() - life_lost_time >= 2000:
            player.x = 300
            player.y = 0
            player.speed = 0
            if is_debug:
                coins = get_debug_coins(coin_frames) # adding back the coins if we lose a life for debug
            game_state = "playing"
    elif game_state == "lose":
        if not sound_played:
            sounds["game_over"].play()
            sound_played = True
        screen.fill(DARK_GREY)
       # draw lose text
        drawText(screen, font, "GAME OVER", WIDTH // 2, HEIGHT // 2, align="center")

    # flip
    pygame.display.flip()
    clock.tick(FPS)

# quit
pygame.quit()