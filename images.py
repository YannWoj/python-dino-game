# images.py
import pygame

# Coins animation frames
coin_frames = [
    pygame.image.load("assets/images/bonus/coins/coin0.png"),
    pygame.image.load("assets/images/bonus/coins/coin1.png"),
    pygame.image.load("assets/images/bonus/coins/coin2.png"),
    pygame.image.load("assets/images/bonus/coins/coin3.png"),
    pygame.image.load("assets/images/bonus/coins/coin4.png"),
    pygame.image.load("assets/images/bonus/coins/coin5.png"),
]

# Single coin image (pour affichage score par exemple)
coin_image = coin_frames[0]

# Enemy images
enemy_image = pygame.image.load("assets/images/enemies/spikes/spike_monster_B.png")

# Hearts and lives
heart_image_32 = pygame.image.load("assets/images/bonus/hearts/heart_32x32.png")
lives_image = pygame.image.load("assets/images/bonus/lives/lives.png")