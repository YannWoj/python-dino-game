# level_loader.py
import pytmx
from pytmx.util_pygame import load_pygame
import pygame
from collectibles.coin_collectible import Coin
from collectibles.life_collectible import Life
from collectibles.heart_collectible import Heart

# load a level (.tmx) and return all objects and tiles
def load_level(tmx_path, coin_frames, life_image, heart_image):
    print(f"[INFO] Loading TMX file: {tmx_path}")
    try:
        # load tmx map
        tmx_data = load_pygame(tmx_path)
    except Exception as e:
        # handle loading errors
        print(f"[ERROR] Failed to load TMX file: {e}")
        return [], [], [], [], [], []

    platforms = []
    coins = []
    enemies = []
    lives = []
    hearts = []
    tiles = []

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer.tiles():
                if gid:
                    # gid can be either a Surface or an int, handle both cases
                    if isinstance(gid, pygame.Surface):
                        tile_image = gid
                    else:
                        tile_image = tmx_data.get_tile_image_by_gid(gid)

                    if not tile_image:
                        continue

                    # get the size of the current tile image to compute correct positions
                    tile_width = tile_image.get_width()
                    tile_height = tile_image.get_height()

                    pos = (x * tile_width, y * tile_height)

                    if layer.name == "Background":
                        # if this is background, it will display first
                        tiles.insert(0, (tile_image, pos))
                    else:
                        tiles.append((tile_image, pos))

                    # collision for platforms
                    if layer.name == "Platforms":
                        rect = pygame.Rect(*pos, tile_width, tile_height)
                        platforms.append(rect)

    # load objects
    for obj in tmx_data.objects:
        if obj.name == "Platform":
            platforms.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        elif obj.name == "Coin":
            coins.append(Coin(obj.x, obj.y, coin_frames))
        elif obj.name == "Enemy":
            enemies.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        elif obj.name == "Life":
            lives.append(Life(obj.x, obj.y, life_image))
        elif obj.name == "Heart":
            hearts.append(Heart(obj.x, obj.y, heart_image))

    # debug print
    print(f"[INFO] Loaded {len(platforms)} platforms, {len(tiles)} tiles, {len(coins)} coins, {len(enemies)} enemies, {len(lives)} lives, {len(hearts)} hearts")
    return platforms, coins, enemies, lives, hearts, tiles


def load_level_tmx(filename):
    tmx_data = pytmx.load_pygame(filename)
    platforms = []

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Platforms":
            for x, y, gid in layer.tiles():
                if gid:
                    # same check for gid type
                    if isinstance(gid, pygame.Surface):
                        tile_image = gid
                        tile_width = tile_image.get_width()
                        tile_height = tile_image.get_height()
                    else:
                        tile_image = tmx_data.get_tile_image_by_gid(gid)
                        if not tile_image:
                            continue
                        tile_width = tile_image.get_width()
                        tile_height = tile_image.get_height()

                    rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
                    platforms.append(rect)

    return platforms, tmx_data