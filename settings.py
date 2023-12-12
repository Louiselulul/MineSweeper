"""
This code is for game settings.
1. Color setting
2. Game default values setting
3. Import tiles
"""

import pygame
import os

# Color settings
white = (255, 255, 255)
black = (0, 0, 0)
darkgrey = (40, 40, 40)
lightgrey = (100, 100, 100)
green = (0, 255, 0)
darkgreen = (0, 200, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
bg_color = darkgrey

# Game default values setting
tile_size = 32
row = 15
col = 15
num_mine = 5
width = tile_size * row
height = tile_size * col
FPS = 60
title = "Minesweeper Game"

# Import all the tiles from the assets folder
tile_list = []
filename = "assets"
for i in range(1, 9):  # since mine number is up to 8
    # resize tile img we have to fit the tile size in our game which is a square
    tile_list.append(pygame.transform.scale
                     (pygame.image.load(os.path.join(filename, f"Tile{i}.png")),
                      (tile_size, tile_size)))
tile_blank = (pygame.transform.scale
              (pygame.image.load(os.path.join(filename, "TileEmpty.png")), (tile_size, tile_size)))
tile_mine_explode = (pygame.transform.scale
                     (pygame.image.load(os.path.join(filename, "TileExploded.png")), (tile_size, tile_size)))
tile_flag = (pygame.transform.scale
             (pygame.image.load(os.path.join("assets", "TileFlag.png")), (tile_size, tile_size)))
tile_mine = (pygame.transform.scale
             (pygame.image.load(os.path.join("assets", "TileMine.png")), (tile_size, tile_size)))
tile_unknown = (pygame.transform.scale
                (pygame.image.load(os.path.join("assets", "TileUnknown.png")), (tile_size, tile_size)))
tile_mine_wrong = (pygame.transform.scale
                   (pygame.image.load(os.path.join("assets", "TileNotMine.png")), (tile_size, tile_size)))
