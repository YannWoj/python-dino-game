# player.py
import pygame

class Player:
    def __init__(self, x=300, y=0):
        self.image = pygame.image.load("assets/images/characters/vita_00.png")
        self.x = x
        self.y = y
        self.speed = 0.0
        self.acceleration = 0.35
        self.width = 45
        self.height = 51
        self.on_ground = False
        self.direction = "right"

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if self.direction == "right":
            screen.blit(self.image, (self.x, self.y))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x, self.y))

        # draw red collision rectangle for the player (to delete later)
        pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 1)

    def update(self, platforms):
        # applying gravity
        self.speed += self.acceleration
        new_y = self.y + self.speed

        # checking vertical collisions
        player_rect = pygame.Rect(self.x, new_y, self.width, self.height)
        self.on_ground = False

        for p in platforms:
            if p.colliderect(player_rect):
                self.speed = 0
                if p.top > self.y:  # platform below
                    self.y = p.top - self.height
                    self.on_ground = True
                break
        else:
            self.y = new_y

    def move_left(self):
        self.x -= 5
        self.direction = "left"

    def move_right(self):
        self.x += 5
        self.direction = "right"

    def jump(self):
        self.speed = -9
