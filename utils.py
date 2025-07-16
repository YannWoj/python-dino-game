# utils.py
import pygame
from constants import MUSTARD, DARK_GREY, WIDTH, HEIGHT

def drawText(screen, font, text_to_draw, x, y, align="topleft"):
    text = font.render(text_to_draw, True, MUSTARD, DARK_GREY)
    text_rect = text.get_rect()
    setattr(text_rect, align, (x, y))
    screen.blit(text, text_rect)

def create_coins(engine, coin_frames):
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
    return [engine.Coin(x, y, coin_frames) for x, y in positions]