# enemies.py
import pygame
from constants import HEIGHT

# returns a list of enemy hitboxes
def get_enemies():
    return [
        pygame.Rect(150, 274, 50, 26),
        pygame.Rect(400, 274, 50, 26),
        pygame.Rect(400, HEIGHT - 56, 50, 26),
        pygame.Rect(150, HEIGHT - 56, 50, 26),
    ]