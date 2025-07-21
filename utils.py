# utils.py
import pygame
from constants import MUSTARD

# draw text on screen
def drawText(screen, font, text_to_draw, x, y, color=MUSTARD, align="topleft"): 
    text = font.render(text_to_draw, True, color)
    text_rect = text.get_rect()
    setattr(text_rect, align, (x, y))
    screen.blit(text, text_rect)