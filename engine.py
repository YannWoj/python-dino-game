# engine.py
import pygame

# handle sprite animations from a list of frames
class Animation():
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 4

    # update animation frame based on timer
    def update(self):
        self.animationTimer += 1
        if self.animationTimer > self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex = (self.imageIndex + 1) % len(self.imageList)
    # draw the current frame at (x, y)
    def draw(self, screen, x, y):
        self.update()
        screen.blit(self.imageList[self.imageIndex], (x, y))

# coin object with animated sprite
class Coin():
    def __init__(self, x, y, animation_frames):
        self.rect = pygame.Rect(x, y, 23, 23)
        self.animation = Animation(animation_frames)

    def draw(self, screen):
        # draw the coin's current animation frame
        self.animation.draw(screen, self.rect.x, self.rect.y)