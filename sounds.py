# sound.py
import pygame

def load_sounds():
    return {
        "coin": pygame.mixer.Sound("assets/sounds/bonus/coins/coin_sound.wav"),
        "jump": pygame.mixer.Sound("assets/sounds/jumps/player_jump.wav"),
        "hit": pygame.mixer.Sound("assets/sounds/damages/hit-damage.wav"),
        "level_completed": pygame.mixer.Sound("assets/sounds/level_completed/level_completed.wav"),
        "lose_life": pygame.mixer.Sound("assets/sounds/fails/lose_life/lose_life.wav"),
        "extra_life": pygame.mixer.Sound("assets/sounds/bonus/extra_life/extra_life.wav"),
        "game_over": pygame.mixer.Sound("assets/sounds/fails/game_over/game_over.wav"),
        "heart_pickup": pygame.mixer.Sound("assets/sounds/bonus/hearts/hearts.wav"),
        "home_select": pygame.mixer.Sound("assets/sounds/menu/home_select.wav")
    }