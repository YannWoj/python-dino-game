# collectibles/coin_collectible.py
import pygame

class Coin:
    def __init__(self, x, y, animation):
        self.x = x
        self.y = y
        self.animation = animation
        self.rect = pygame.Rect(x, y, 32, 32)

    def update(self):
        self.animation.update()

    def draw(self, screen):
        frame = self.animation.imageList[self.animation.imageIndex]
        screen.blit(frame, (self.x, self.y))