# the meal for the snake

import random
from constants import playfieldsize_x, playfieldsize_y
import pygame

x = 0
y = 0


def get_mealcoord():
    global x, y
    return (x, y)


def generate_new_position():
    """generates new random position for the meal."""
    global x, y
    x = random.randint(0, playfieldsize_x - 1)
    y = random.randint(0, playfieldsize_y - 1)


def getposition():
    global x, y
    return (x, y)


# initiate
generate_new_position()


def draw(surf: pygame.Surface):
    """Draws the meal onto given surface"""
    from constants import pixelcoord_in_playfield, mealcolor
    from constants import tilesize_x, tilesize_y

    global x, y
    mealpos_px = pixelcoord_in_playfield((x, y))
    mealpos_x, mealpos_y = mealpos_px

    pygame.draw.rect(
        surf, mealcolor, pygame.Rect(mealpos_x, mealpos_y, tilesize_x, tilesize_y)
    )
