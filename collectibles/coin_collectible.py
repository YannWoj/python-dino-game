# collectibles/coin_collectible.py
import pygame
from animation import Animation
from images import coin_frames

class Coin:
    def __init__(self, x, y, animation):
        self.x = x
        self.y = y
        self.animation = Animation(coin_frames, frame_duration=90)
        self.rect = pygame.Rect(x, y, 32, 32) # create a collision rectangle based on the image size

    def update(self):
        self.animation.update()

    def draw(self, screen):
        self.animation.update()
        frame = self.animation.get_current_frame()
        screen.blit(frame, (self.x, self.y))