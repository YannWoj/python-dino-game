import pygame
import animation
from images import jump_image

class Player:
    def __init__(self, x=300, y=0):
        self.image = pygame.image.load("assets/images/characters/vita_00.png")
        self.x = float(x)
        self.y = float(y)
        self.speed = 0.0
        self.acceleration = 0.40  # gravity
        self.width = 45
        self.height = 51
        self.on_ground = False
        self.direction = "right"
        self.state = "idle"  # or "walking"
        self.hurt_timer = 0
        self.invincible_timer = 0  # timer for invincibility
        self.is_invincible = False  # invincibility state
        self.blink_interval = 100  # blink interval in ms
        self.last_blink = 0  # last blink toggle time
        self.visible = True  # controls whether the player is visible or not
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.animations = { 
            "idle" : animation.Animation([
                pygame.image.load("assets/images/characters/vita_00.png"),
                pygame.image.load("assets/images/characters/vita_01.png"),
                pygame.image.load("assets/images/characters/vita_02.png"),
                pygame.image.load("assets/images/characters/vita_03.png")
            ], frame_duration=100),
            "walking" : animation.Animation([
                pygame.image.load("assets/images/characters/vita_04.png"),
                pygame.image.load("assets/images/characters/vita_05.png"),
                pygame.image.load("assets/images/characters/vita_06.png"),
                pygame.image.load("assets/images/characters/vita_07.png"),
                pygame.image.load("assets/images/characters/vita_08.png"),
                pygame.image.load("assets/images/characters/vita_09.png")
            ], frame_duration=100),
            "hurt" : animation.Animation([
                pygame.image.load("assets/images/characters/vita_14.png"),
                pygame.image.load("assets/images/characters/vita_15.png"),
                pygame.image.load("assets/images/characters/vita_16.png")
            ], frame_duration=50)  # faster animation for "hurt"
        }

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, screen, camera=None):
        # only draw if the player is visible (for blinking effect)
        if not self.visible:
            return

        if self.state == "jumping":
            frame = jump_image
        else:
            current_animation = self.animations[self.state]
            current_animation.update()
            frame = current_animation.get_current_frame()
            
        # get the camera offset
        if camera:
            draw_rect = camera.apply(self.get_rect())
            draw_pos = (draw_rect.x, draw_rect.y)
        else:
            draw_pos = (int(self.x), int(self.y))
        
        if self.direction == "right":
            screen.blit(frame, draw_pos)
        else:
            flipped_frame = pygame.transform.flip(frame, True, False)
            screen.blit(flipped_frame, draw_pos)

        # draw red collision rectangle for the player (to delete later)
        # if camera:
        #     pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.get_rect()), 1)
        # else:
        #     pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 1)

    def update(self, platforms: list, dx: float = 0, dy: float = 0):
        # handle blinking during invincibility
        if self.is_invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_blink > self.blink_interval:
                self.visible = not self.visible  # toggle visible/invisible
                self.last_blink = current_time

        # attempt horizontal movement
        new_x = self.x + dx
        player_rect = pygame.Rect(new_x, self.y, self.width, self.height)
        collision_x = False

        for p in platforms:
            if p.colliderect(player_rect):
                collision_x = True
                break

        if not collision_x:
            self.x = new_x

        # apply gravity
        self.speed += self.acceleration
        new_y = self.y + self.speed + dy

        player_rect = pygame.Rect(self.x, new_y, self.width, self.height)
        self.on_ground = False
        collision_y = False

        # check if player collides vertically with any platform
        for p in platforms:
            if p.colliderect(player_rect):
                collision_y = True
                if self.speed >= 0 and self.y + self.height <= p.top + 10:
                    self.y = p.top - self.height
                    self.on_ground = True
                    self.speed = 0
                break

        if not collision_y:
            self.y = new_y

        # check if player is hurt and enough time has passed
        if self.state == "hurt":
            if pygame.time.get_ticks() - self.hurt_timer > 300:  # 0.3 seconds for hurt state
                self.state = "idle"
                self.is_invincible = True
                self.invincible_timer = pygame.time.get_ticks()
                self.last_blink = pygame.time.get_ticks()
                self.visible = True

        # check if invincibility has ended
        if self.is_invincible:
            if pygame.time.get_ticks() - self.invincible_timer > 750:  # 0.75 second of invincibility
                self.is_invincible = False
                self.visible = True

        # set state to jumping if the player is in the air and moving upward
        if not self.on_ground and self.speed < 0:
            self.state = "jumping"
        elif self.on_ground and self.state == "jumping":
            self.state = "idle"
            
        self.rect = self.get_rect()

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
        self.speed = -8.4  # height of the jump