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
    new_player_x = player_x
    keys = pygame.key.get_pressed() # Held (maintenues) keys (True/False)

    if keys[pygame.K_LEFT]:
        new_player_x -= 5
    if keys[pygame.K_RIGHT]:
        new_player_x += 5

    # horizontal movement
    new_player_rect = pygame.Rect(new_player_x, 200, 72, 72)
    x_collision = False

    # check against every platform
    for p in platforms:
        if p.colliderect(new_player_rect):
            x_collision = True
            break

    # set x_collision to true
    if x_collision == False:
        player_x = new_player_x
    
    # update
    
    # draw
    # background
    screen.fill(DARK_GREY)
    # platforms
    for p in platforms:
        pygame.draw.rect(screen, (MUSTARD), p)
    
    # present screen
    screen.blit(player_image, (player_x, 200))
    pygame.draw.rect(screen, (255, 0, 0), (player_x, 200, 72, 72), 1)
    pygame.display.flip()

    clock.tick(60)

# quit
pygame.quit()