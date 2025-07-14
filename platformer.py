# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# X account : @ScissorMarks
# Coin sprite bt DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0
# Spike sprites by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters

import pygame
import math

def drawText(text_to_draw, x, y, align="topleft"):
    text = font.render(text_to_draw, True, MUSTARD, DARK_GREY)
    text_rect = text.get_rect()
    setattr(text_rect, align, (x, y))
    screen.blit(text, text_rect)

# constant variables
WIDTH = 700
HEIGHT = 500
DARK_GREY = (50, 50, 50)
MUSTARD = (209, 206, 25)

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

# player
player_image = pygame.image.load("assets/images/characters/vita_00.png")
player_x = 300

player_y = 0
player_speed = 0
player_acceleration = 0.35

player_width = 45
player_height = 51

player_on_ground = False

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
coin_images = [
    pygame.image.load(f"assets/images/bonus/coins/coin{i}.png") for i in range(6)
    ]
coins = [
    pygame.Rect(220, 260, 23, 23),
    pygame.Rect(460, 220, 23, 23),
    pygame.Rect(120, 220, 23, 23),
    pygame.Rect(WIDTH - 100, HEIGHT - 200, 23, 23),
    pygame.Rect(WIDTH - 80, HEIGHT - 230, 23, 23),
    pygame.Rect(WIDTH - 60, HEIGHT - 260, 23, 23),
    pygame.Rect(150 + 16, HEIGHT - 90, 23, 23),
    pygame.Rect(400 + 16, HEIGHT - 90, 23, 23),
    pygame.Rect(290, HEIGHT - 130, 23, 23),
    pygame.Rect(38, (HEIGHT // 2) + 50, 23, 23)
]

coin_frame = 0
coin_frame_timer = 0

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

# score & life
score = 0
lives = 3

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
        if keys[pygame.K_RIGHT]:
            new_player_x += 5
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
        # print(player_y)
        # print(player_speed)

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
        # print(player_on_ground)

        if y_collision == False:
            player_y = new_player_y

        # see if any coins have been collected
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for coin in coins:
            if coin.colliderect(player_rect):
                coins.remove(coin) # from the list
                score+=1
                coin_sound.play()
                # win if the score is 10
                if score >= 10:
                    game_state = "win" 
                
        # see if the player has hit an enemy
        for enemy in enemies:
            if enemy.colliderect(player_rect):
                lives-=1
                hit_damage_sound.play()
                # reset player position
                player_x = 300
                player_y = 0
                player_speed = 0
                # change the game state
                if lives <= 0:
                    game_state = "lose"

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
        screen.blit(player_image, (player_x, player_y))
        # player rect
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height), 1)

        # coins
        for coin in coins:
            float_offset = math.sin(pygame.time.get_ticks() / 500) * 2.5
            screen.blit(coin_images[coin_frame], (coin[0], coin[1] + float_offset))

        # coin animation timing
        coin_frame_timer += 1
        if coin_frame_timer >= 4:
            coin_frame = (coin_frame + 1) % len(coin_images)
            coin_frame_timer = 0

        # enemies
        for enemy in enemies:
            screen.blit(enemy_image, (enemy.x, enemy.y))

        # player informations
        # lives
        for i in range(lives):
            screen.blit(heart_image_32, (10 + i * (heart_image_32.get_width() + 5), 10))

        # score
        drawText("Score: " + str(score), WIDTH - 10, 10, "topright")

    if game_state == "win":
        # settings
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(DARK_GREY)
        screen.blit(overlay, (0, 0))
        # draw win text
        drawText("YOU WIN!", WIDTH // 2, HEIGHT // 2, "center")
    if game_state == "lose":
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