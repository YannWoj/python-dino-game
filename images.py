# images.py
import pygame

# title image
title_image = pygame.image.load("assets/home_screen/dino-platformer.png")
title_image = pygame.transform.scale(title_image, (625, 150))

# coins animation frames
coin_frames = [
    pygame.image.load("assets/images/bonus/coins/coin0.png"),
    pygame.image.load("assets/images/bonus/coins/coin1.png"),
    pygame.image.load("assets/images/bonus/coins/coin2.png"),
    pygame.image.load("assets/images/bonus/coins/coin3.png"),
    pygame.image.load("assets/images/bonus/coins/coin4.png"),
    pygame.image.load("assets/images/bonus/coins/coin5.png"),
]

# single coin image
coin_image = coin_frames[0]

# enemy images
enemy_image = pygame.image.load("assets/images/enemies/spikes/spike_monster_B.png")

# jump
jump_image = pygame.image.load("assets/images/characters/vita_10.png")

# hearts and lives
heart_image_16 = pygame.image.load("assets/images/bonus/hearts/heart_16x16.png")
heart_image_32 = pygame.image.load("assets/images/bonus/hearts/heart_32x32.png")
lives_image = pygame.image.load("assets/images/bonus/lives/lives.png")