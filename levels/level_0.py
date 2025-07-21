# levels/level_0.py, DEBUG
import pygame
from constants import WIDTH, HEIGHT
from collectibles.coin_collectible import Coin
from collectibles.life_collectible import Life
from collectibles.heart_collectible import Heart
from animation import Animation

# returns the platforms for level 0 (debug level)
def get_debug_platforms():
    return [
        pygame.Rect(100, 300, 400, 50),  # middle
        pygame.Rect(100, 250, 50, 50),   # left
        pygame.Rect(450, 250, 50, 50),   # right
        pygame.Rect(0, HEIGHT - 30, WIDTH, 30),  # ground
        pygame.Rect(WIDTH - 120, HEIGHT - 130, 50, 30),
        pygame.Rect(WIDTH - 95, HEIGHT - 155, 50, 30),
        pygame.Rect(WIDTH - 70, HEIGHT - 180, 50, 30),
        pygame.Rect(WIDTH - 150, HEIGHT - 110, 50, 30),
    ]

# returns the coins for level 0
def get_debug_coins(coin_frames):
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
    return [Coin(x, y, Animation(coin_frames)) for x, y in positions]

# returns the lives for level 0
def get_debug_lives(image):
    return [Life(30, 90, image)]

# returns the hearts for level 0
def get_debug_hearts(heart_image):
    return [
        Heart(100, 150, heart_image),
        Heart(300, 250, heart_image),
        Heart(500, 180, heart_image)
    ]

# returns the enemies for level 0
def get_debug_enemies():
    return [
        pygame.Rect(150, 274, 50, 26),
        pygame.Rect(400, 274, 50, 26),
        pygame.Rect(400, HEIGHT - 56, 50, 26),
        pygame.Rect(150, HEIGHT - 56, 50, 26),
    ]