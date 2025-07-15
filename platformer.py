# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# X account : @ScissorMarks
# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0
# Spike sprites by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

import pygame
import math
import engine
from constants import WIDTH, HEIGHT, DARK_GREY, MUSTARD


def drawText(text_to_draw, x, y, align="topleft"):
    text = font.render(text_to_draw, True, MUSTARD, DARK_GREY)
    text_rect = text.get_rect()
    setattr(text_rect, align, (x, y))
    screen.blit(text, text_rect)

def create_coins():
    positions = [
        (220, 260),
        (460, 220),
        (120, 220),
        (WIDTH - 100, HEIGHT - 200),
        (WIDTH - 80, HEIGHT - 230),
        (WIDTH - 60, HEIGHT - 260),
        (150 + 16, HEIGHT - 90),
        (400 + 16, HEIGHT - 90),
        (290, HEIGHT - 130),
        (38, (HEIGHT // 2) + 50),
        (58, (HEIGHT // 2) + 50),
    ]
    return [engine.Coin(x, y, coin_frames) for x, y in positions]

# init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# games states = playing // win // lose
game_state = 'playing'

# sounds
# coin
coin_sound = pygame.mixer.Sound("assets/sounds/bonus/coins/coin_sound.wav")
# hit damage
hit_damage_sound = pygame.mixer.Sound("assets/sounds/damages/hit-damage.wav")
# jump
jump_sound = pygame.mixer.Sound("assets/sounds/jumps/player_jump.wav")
# level completed
level_completed_sound = pygame.mixer.Sound("assets/sounds/level_completed/level_completed.wav")
# losing a life
lose_life_sound = pygame.mixer.Sound("assets/sounds/fails/lose_life/lose_life.wav")
# extra life
extra_life_sound = pygame.mixer.Sound("assets/sounds/bonus/extra_life/extra_life.wav")
# game over
game_over_sound = pygame.mixer.Sound("assets/sounds/fails/game_over/game_over.wav")
game_over_sound.set_volume(0.33)

# player
player_image = pygame.image.load("assets/images/characters/vita_00.png")
player_x = 300

player_y = 0
player_speed = 0
player_acceleration = 0.35

player_width = 45
player_height = 51

player_on_ground = False
player_direction = "right"

# platforms
platforms = [
    # middle
    pygame.Rect(100,300,400,50),
    # left
    pygame.Rect(100,250,50,50),
    # right
    pygame.Rect(450,250,50,50),
    # ground
    pygame.Rect(0, HEIGHT - 30, WIDTH, 30),
    # platforms
    pygame.Rect(WIDTH - 120, HEIGHT - 130, 50, 30),
    pygame.Rect(WIDTH - 95, HEIGHT - 155, 50, 30),
    pygame.Rect(WIDTH - 70, HEIGHT - 180, 50, 30)
]

# coins
coin_image = pygame.image.load("assets/images/bonus/coins/coin0.png")

coin_frames = [
    pygame.image.load("assets/images/bonus/coins/coin0.png"),
    pygame.image.load("assets/images/bonus/coins/coin1.png"),
    pygame.image.load("assets/images/bonus/coins/coin2.png"),
    pygame.image.load("assets/images/bonus/coins/coin3.png"),
    pygame.image.load("assets/images/bonus/coins/coin4.png"),
    pygame.image.load("assets/images/bonus/coins/coin5.png"),
]

coins = create_coins()

# enemies
enemy_image = pygame.image.load("assets/images/enemies/spikes/spike_monster_B.png")

enemies = [
    pygame.Rect(150, 274, 50, 26),
    pygame.Rect(400 ,274, 50, 26),
    pygame.Rect(400 ,HEIGHT - 56, 50, 26),
    pygame.Rect(150 ,HEIGHT - 56, 50, 26)
]

# hearts
heart_image_32 = pygame.image.load("assets/images/bonus/hearts/heart_32x32.png")

# lives
lives_image = pygame.image.load("assets/images/bonus/lives/lives.png")

# score & life
score = 0
lives = 3
hearts = 3
coins_for_life = 0
sound_played = False
win_time = 0
life_lost_time = 0
last_hit_time = 0

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
    new_player_x = player_x
    new_player_y = player_y

    if game_state == "playing":
        # player input
        keys = pygame.key.get_pressed() # Held (maintenues) keys (True/False)

        if keys[pygame.K_LEFT]:
            new_player_x -= 5
            player_direction = "left"
        if keys[pygame.K_RIGHT]:
            new_player_x += 5
            player_direction = "right"
        if keys[pygame.K_SPACE] and player_on_ground:
            player_speed = -8.75
            jump_sound.play()

    # ------
    # UPDATE
    # ------

    if game_state == "playing":
        # horizontal movement
        new_player_rect = pygame.Rect(new_player_x, player_y, player_width, player_height)
        x_collision = False

        # check against every platform
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        # set x_collision to true
        if x_collision == False:
            player_x = new_player_x

        # vertical movement

        player_speed += player_acceleration
        new_player_y += player_speed

        new_player_rect = pygame.Rect(player_x, new_player_y, player_width, player_height)
        y_collision = False
        player_on_ground = False

        for p in platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                # if the platform is below the player
                if p[1] > new_player_y:
                    # stick the player to the platform
                    player_y = p[1] - player_height
                    player_on_ground = True
                break

        if y_collision == False:
            player_y = new_player_y

        # see if any coins have been collected
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
        for coin in coins[:]:
            if coin.rect.colliderect(player_rect):
                coins.remove(coin)  # from the list
                score += 1
                coins_for_life += 1 
                coin_sound.play()
                # gives a life every 10 coins
                if coins_for_life >= 10:
                    lives += 1
                    coins_for_life = 0
                    hearts = 3
                    extra_life_sound.play()
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
                    hit_damage_sound.play()
                    if hearts <= 0:
                        lives -= 1
                        if lives <= 0:
                            game_state = "lose"
                            game_over_sound.play()
                        else:
                            hearts = 3
                            lose_life_sound.play()
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
        if player_direction == "right":
            screen.blit(player_image, (player_x, player_y))
        elif player_direction == "left":
            screen.blit(pygame.transform.flip(player_image, True, False), (player_x, player_y))
        # player rect
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height), 1)

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
        drawText(text_str, text_x, text_y, "topleft")

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
        drawText(score_text, score_x, score_y, "topright")
        screen.blit(coin_image, (coin_x, coin_y))


    if game_state == "win":
        if not sound_played and pygame.time.get_ticks() - win_time > 95:
            level_completed_sound.play()
            sound_played = True
        # settings
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(DARK_GREY)
        screen.blit(overlay, (0, 0))
        # draw win text
        drawText("YOU WIN!", WIDTH // 2, HEIGHT // 2, "center")
    elif game_state == "life_lost":
        # background color 
        screen.fill(DARK_GREY)

        # display lives
        icon_x = WIDTH // 2 - (lives_image.get_width() // 2 + 20)
        icon_y = HEIGHT // 2 - lives_image.get_height() // 2

        screen.blit(lives_image, (icon_x, icon_y))

        text_str = f"x {lives}"
        drawText(text_str, icon_x + lives_image.get_width() + 10, icon_y + 5, "topleft")

        # 2 seconds timer
        if pygame.time.get_ticks() - life_lost_time >= 2000:
            player_x = 300
            player_y = 0
            player_speed = 0
            coins = create_coins() # adding back the coins if we lose a life
            game_state = "playing"
    elif game_state == "lose":
        if not sound_played:
            game_over_sound.play()
            sound_played = True
        # settings
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(DARK_GREY)
        screen.blit(overlay, (0, 0))
        # draw lose text
        drawText("GAME OVER", WIDTH // 2, HEIGHT // 2, "center")

    # flip
    pygame.display.flip()
    clock.tick(60)

# quit
pygame.quit()