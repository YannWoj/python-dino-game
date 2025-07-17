# player.py
import pygame
import engine
from images import jump_image

class Player:
    def __init__(self, x=300, y=0):
        self.image = pygame.image.load("assets/images/characters/vita_00.png")
        self.x = float(x)
        self.y = float(y)
        self.speed = 0.0
        self.acceleration = 0.35
        self.width = 45
        self.height = 51
        self.on_ground = False
        self.direction = "right"
        self.state = "idle" # or "walking"
        self.hurt_timer = 0
        self.animations = { 
                           "idle" : engine.Animation([
                                    pygame.image.load("assets/images/characters/vita_00.png"),
                                    pygame.image.load("assets/images/characters/vita_01.png"),
                                    pygame.image.load("assets/images/characters/vita_02.png"),
                                    pygame.image.load("assets/images/characters/vita_03.png")
                                ]),
                           "walking" : engine.Animation([
                                    pygame.image.load("assets/images/characters/vita_04.png"),
                                    pygame.image.load("assets/images/characters/vita_05.png"),
                                    pygame.image.load("assets/images/characters/vita_06.png"),
                                    pygame.image.load("assets/images/characters/vita_07.png"),
                                    pygame.image.load("assets/images/characters/vita_08.png"),
                                    pygame.image.load("assets/images/characters/vita_09.png"),
                                ]),
                           "hurt" : engine.Animation([
                                pygame.image.load("assets/images/characters/vita_14.png"),
                                pygame.image.load("assets/images/characters/vita_15.png"),
                                pygame.image.load("assets/images/characters/vita_16.png")
                                ])
                           }
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen):
        if self.state == "jumping":
            frame = jump_image
        else:
            current_animation = self.animations[self.state]
            current_animation.update()
            frame = current_animation.imageList[current_animation.imageIndex]
        
        if self.direction == "right":
            screen.blit(frame, (int(self.x), int(self.y)))
        else:
            flipped_frame = pygame.transform.flip(frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

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

        # check if player is hurt and enough time has passed
        if self.state == "hurt":
            if pygame.time.get_ticks() - self.hurt_timer > 1000:  # 1 seconde
                self.state = "idle"

        # set state to jumping if the player is in the air and going up
        if not self.on_ground and self.speed < 0:
            self.state = "jumping"
        elif self.on_ground and self.state == "jumping":
            self.state = "idle"

    # moving to the left
    def move_left(self):
        self.x -= 5
        self.direction = "left"
    # moving to the right
    def move_right(self):
        self.x += 5
        self.direction = "right"
    # jumping
    def jump(self):
        self.speed = -8.5
