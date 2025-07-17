# utils.py
import pygame
from constants import MUSTARD, DARK_GREY, WIDTH, HEIGHT
from collectibles.heart_collectible import Heart

# draw text on screen
def drawText(screen, font, text_to_draw, x, y, align="topleft"):
    text = font.render(text_to_draw, True, MUSTARD, DARK_GREY)
    text_rect = text.get_rect()
    setattr(text_rect, align, (x, y))
    screen.blit(text, text_rect)

# create coins at fixed positions
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

# create lives
def create_lives(image):
    positions = [
        (30, 90),
    ]
    from collectibles.life_collectible import Life
    return [Life(x, y, image) for x, y in positions]

def create_hearts(heart_image):
    positions = [
        (100, 150),
        (300, 250),
        (500, 180)
    ]
    return [Heart(x, y, heart_image) for x, y in positions]