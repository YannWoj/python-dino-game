# sound.py
import pygame

def load_sounds():
    return {
        # coin sound
        "coin": pygame.mixer.Sound("assets/sounds/bonus/coins/coin_sound.wav"),
        # jump sound
        "jump": pygame.mixer.Sound("assets/sounds/jumps/player_jump.wav"),
        # hit sound
        "hit": pygame.mixer.Sound("assets/sounds/damages/hit-damage.wav"),
        # level completed sound
        "level_completed": pygame.mixer.Sound("assets/sounds/level_completed/level_completed.wav"),
        # lose life sound
        "lose_life": pygame.mixer.Sound("assets/sounds/fails/lose_life/lose_life.wav"),
        # extra life sound
        "extra_life": pygame.mixer.Sound("assets/sounds/bonus/extra_life/extra_life.wav"),
        # game over sound
        "game_over": pygame.mixer.Sound("assets/sounds/fails/game_over/game_over.wav"),
        # heart pickup sound
        "heart_pickup": pygame.mixer.Sound("assets/sounds/bonus/hearts/hearts.wav"),
        # home select sound
        "home_select": pygame.mixer.Sound("assets/sounds/menu/home_select.wav")
    }