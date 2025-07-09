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

# player
player_image = pygame.image.load("assets/images/vita_00.png")

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

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    
    # draw
    # background
    screen.fill(DARK_GREY)
    # platforms
    for p in platforms:
        pygame.draw.rect(screen, (MUSTARD), p)
    
    # present screen
    screen.blit(player_image, (300, 100))
    pygame.display.flip()

# quit
pygame.quit()