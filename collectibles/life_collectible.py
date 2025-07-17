# collectibles/life_collectible.py
import pygame

class Life:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))