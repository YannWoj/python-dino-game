# level_manager.py
from level_loader import load_level

# load and return all level data from .tmx file
def load_level_data(level_path, coin_frames, life_image, heart_image):
    platforms, coins, enemies, lives, hearts, tiles = load_level(
        level_path, coin_frames, life_image, heart_image
    )
    return platforms, coins, enemies, lives, hearts, tiles