# collectibles/life_collectible.py
import pygame

class Life:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height()) # create a collision rectangle based on the image size

    def draw(self, screen):
        # draw the life collectible on the screen
        screen.blit(self.image, (self.x, self.y))