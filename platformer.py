# Dinosaur player images by Arks
# https://arks.itch.io/dino-characters
# X account : @ScissorMarks

import pygame

# constant variables
WIDTH = 700
HEIGHT = 500
DARK_GREY = (50, 50, 50)
MUSTARD = (209, 206, 25)

# init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

# player
player_image = pygame.image.load("assets/images/vita_00.png")
player_x = 300

# platforms
platforms = [
    # middle
    pygame.Rect(100,300,400,50),
    # left
    pygame.Rect(100,250,50,50),
    # right
    pygame.Rect(450,250,50,50)
]

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

    # player input
    keys = pygame.key.get_pressed() # Held (maintenues) keys (True/False)

    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5

    # update
    
    # draw
    # background
    screen.fill(DARK_GREY)
    # platforms
    for p in platforms:
        pygame.draw.rect(screen, (MUSTARD), p)
    
    # present screen
    screen.blit(player_image, (player_x, 100))
    pygame.display.flip()

    clock.tick(60)

# quit
pygame.quit()