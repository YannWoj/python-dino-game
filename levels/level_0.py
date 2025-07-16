# level_0.py
import pygame
from constants import WIDTH, HEIGHT

# Returns the platforms for level 0
def get_platforms():
    return [
        pygame.Rect(100, 300, 400, 50),  # middle
        pygame.Rect(100, 250, 50, 50),   # left
        pygame.Rect(450, 250, 50, 50),   # right
        pygame.Rect(0, HEIGHT - 30, WIDTH, 30),  # ground
        pygame.Rect(WIDTH - 120, HEIGHT - 130, 50, 30),
        pygame.Rect(WIDTH - 95, HEIGHT - 155, 50, 30),
        pygame.Rect(WIDTH - 70, HEIGHT - 180, 50, 30),
    ]