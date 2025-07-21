# animation.py
import pygame

# handle sprite animations from a list of frames
class Animation:
    def __init__(self, frames, frame_duration=100):
        self.frames = frames
        self.frame_duration = frame_duration  # Durée d'une frame (en ms)
        self.current_time = 0
        self.current_frame_index = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_duration:
            self.last_update = now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame_index]