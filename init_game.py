# init_game.py
import pygame
from constants import WIDTH, HEIGHT

def init():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Platformer")
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/fonts/ARCADE_N.TTF", 24)
    return screen, clock, font