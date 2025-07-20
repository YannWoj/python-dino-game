# levels/level_1.py
from level_loader import load_level, load_level_tmx

# load level 1 platforms from the .tmx file
def get_platforms():
    platforms, _ = load_level_tmx("levels/tmx/level_1.tmx")
    return platforms