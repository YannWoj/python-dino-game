# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# X account : @ScissorMarks
# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0
# Spike sprites by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

# main
# imports
import pygame
import math
import engine
from constants import WIDTH, HEIGHT, DARK_GREY, MUSTARD, FPS
from player import Player
from levels.level_0 import get_platforms
from enemies import get_enemies
from sound import load_sounds
from images import coin_frames, coin_image, enemy_image, heart_image_32, lives_image
from init_game import init
from utils import drawText, create_coins

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

# games states = playing // win // lose
game_state = 'playing'

# sounds
sounds = load_sounds()
sounds["game_over"].set_volume(0.33)

# player
player = Player()

# platforms
platforms = get_platforms()

# coins
coins = create_coins(engine, coin_frames)

# enemies
enemies = get_enemies()

running = True
while running:
# game loop

    # -----
    # INPUT
    # -----

    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # simulating x and y positions
    new_player_x = player.x
    new_player_y = player.y

    if game_state == "playing":
        # player input
        keys = pygame.key.get_pressed() # Held (maintenues) keys (True/False)

        if keys[pygame.K_LEFT]:
            new_player_x -= 3.5
            player.direction = "left"
            player.state = "walking"
        if keys[pygame.K_RIGHT]:
            new_player_x += 3.5
            player.direction = "right"
            player.state = "walking"
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.state = "idle"
        if keys[pygame.K_SPACE] and player.on_ground:
            player.jump()
            sounds["jump"].play()
        print(player.state)
            
        player.update(platforms)

    # ------
    # UPDATE
    # ------

    if game_state == "playing":
        # horizontal movement
        new_player_rect = pygame.Rect(new_player_x, player.y, player.width, player.height)
        x_collision = False

        # check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        # set x_collision to true
        if not x_collision:
            player.x = new_player_x

        # see if any coins have been collected
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        
        for coin in coins[:]:
            if coin.rect.colliderect(player_rect):
                coins.remove(coin)  # from the list
                score += 1
                coins_for_life += 1 
                sounds["coin"].play()
                # gives a life every 10 coins
                if coins_for_life >= 10:
                    lives += 1
                    coins_for_life = 0
                    hearts = 3
                    sounds["extra_life"].play()
                # win if all coins are collected
                if len(coins) == 0:
                    game_state = "win"
                    win_time = pygame.time.get_ticks()  # Record the time when the player wins
                
        # see if the player has hit an enemy
        for enemy in enemies:
            if enemy.colliderect(player_rect):
                current_time = pygame.time.get_ticks()
                # 1 sec cooldown to avoid instant multiple hits
                if current_time - last_hit_time >= 1000:
                    last_hit_time = current_time
                    hearts -= 1
                    sounds["hit"].play()
                    if hearts <= 0:
                        lives -= 1
                        if lives <= 0:
                            game_state = "lose"
                            sounds["game_over"].play()
                        else:
                            hearts = 3
                            sounds["lose_life"].play()
                            coins_for_life = 0
                            game_state = "life_lost"
                            life_lost_time = pygame.time.get_ticks()
                break
    # ----
    # DRAW
    # ----
    # background
    screen.fill(DARK_GREY)
        
    if game_state == "playing":
        # platforms
        for p in platforms:
            pygame.draw.rect(screen, (MUSTARD), p)
        
        # player
        player.draw(screen)

        # coins
        for coin in coins:
            coin.draw(screen)
        # enemies
        for enemy in enemies:
            screen.blit(enemy_image, (enemy.x, enemy.y))

        # player informations
        # lives icon with count
        icon_x = 10
        icon_y = 10

        # draw the player face icon (number of lives)
        screen.blit(lives_image, (icon_x, icon_y))

        # draw the "x N" next to the face icon
        text_x = icon_x + lives_image.get_width() + 5
        text_y = icon_y + 5
        text_str = f"x {lives}"
        drawText(screen, font, text_str, text_x, text_y, align="topleft")

        # calculate text width to place hearts after it
        text_surface = font.render(text_str, True, MUSTARD)
        text_width = text_surface.get_width()

        # draw hearts next to the text
        for i in range(hearts):
            heart_x = text_x + text_width + 15 + i * (heart_image_32.get_width() + 5)
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
        drawText(screen, font, score_text, score_x, score_y, align="topright")
        screen.blit(coin_image, (coin_x, coin_y))


    if game_state == "win":
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
    elif game_state == "life_lost":
        # background color 
        screen.fill(DARK_GREY)

        # display lives
        icon_x = WIDTH // 2 - (lives_image.get_width() // 2 + 20)
        icon_y = HEIGHT // 2 - lives_image.get_height() // 2

        screen.blit(lives_image, (icon_x, icon_y))

        text_str = f"x {lives}"
        drawText(screen, font, text_str, icon_x + lives_image.get_width() + 10, icon_y + 5, align="topleft")

        # 2 seconds timer
        if pygame.time.get_ticks() - life_lost_time >= 2000:
            player.x = 300
            player.y = 0
            player.speed = 0
            coins = coins = create_coins(engine, coin_frames) # adding back the coins if we lose a life
            game_state = "playing"
    elif game_state == "lose":
        if not sound_played:
            sounds["game_over"].play()
            sound_played = True
        # settings
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(DARK_GREY)
        screen.blit(overlay, (0, 0))
        # draw lose text
        drawText(screen, font, "GAME OVER", WIDTH // 2, HEIGHT // 2, align="center")

    # flip
    pygame.display.flip()
    clock.tick(FPS)

# quit
pygame.quit()