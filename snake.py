# module that controls the snake
import pygame

from typing import Tuple

# current direction is saved as int. 0=left, 2=right, 1=up, 3=down.
# this makes sure even values are horizontal and odd are vertical
current_direction = 2


def print_direction():
    """Prints current moving direction of the snake to console."""
    global current_direction

    if current_direction == 0:
        print("left")
    elif current_direction == 1:
        print("up")
    elif current_direction == 2:
        print("right")
    elif current_direction == 3:
        print("down")


def set_direction(new_dir: str):
    """sets direction to left/right/up/down. Raises ValueError
    if given parameter is not one of these."""
    global current_direction

    if new_dir == "left":
        current_direction = 0
    elif new_dir == "right":
        current_direction = 2
    elif new_dir == "up":
        current_direction = 1
    elif new_dir == "down":
        current_direction = 3
    else:
        raise ValueError("Trying to set direction to not-allowed value " + new_dir)


# True if the game is currently paused
paused = False


def get_pause_state():
    """True if paused, False if running"""
    global paused
    return paused


def toggle_pause():
    """Pauses if currently running, unpauses if currently paused"""
    global paused
    paused = not paused


headcoord = (3, 3)


def get_headcoord():
    global headcoord
    return headcoord


# tail is reversed, last position of the snake comes first.
tail = [(3, 2)]

# number of ticks to wait until next move
from constants import ticks_per_move

move_delay = ticks_per_move


def tick():
    """advances the game state by one tick"""
    global move_delay, headcoord, tail, current_direction
    move_delay -= 1
    if move_delay > 0:
        return
    move_delay = ticks_per_move

    # move snake
    headx, heady = headcoord
    if current_direction == 0:  # left
        headx = headx - 1
    elif current_direction == 2:  # right
        headx = headx + 1
    elif current_direction == 1:  # up
        heady = heady - 1
    elif current_direction == 3:  # down
        heady = heady + 1
    else:
        raise ValueError("internal direction var is broken!")

    tail.append(headcoord)
    headcoord = (headx, heady)

    # snake should only become longer if the meal was reached. Remove the oldest
    # entry in tail (which is at position 0 since headcoord is appended at the end)
    import meal

    if headcoord == meal.getposition():
        meal.generate_new_position()
    else:
        tail.remove(tail[0])


def check_collision():
    """True if the head collided with any part of the tail"""
    global headcoord, tail
    return headcoord in tail


def check_boundaries():
    """True if the head is outside of the playfield"""
    global headcoord
    from constants import playfieldsize_x, playfieldsize_y

    x, y = headcoord
    if x < 0 or y < 0:
        return True
    elif x > playfieldsize_x or y > playfieldsize_y:
        return True
    return False


def check_alive():
    """False if the snake is in a losing position: Head colliding with
    the wall or with the tail"""
    return not (check_collision() or check_boundaries())


def occupies_tile(coords: Tuple[int]):
    """True if the given tile is occupied by the snake"""
    global headcoord, tail
    if coords == headcoord:
        return True
    else:
        return coords in tail


def getlength():
    """Total length of the snake"""
    global tail
    return 1 + len(tail)


def draw(surf: pygame.Surface):
    """draws the snake to given surface"""
    from constants import pixelcoord_in_playfield, snakeheadcolor, snaketailcolor
    from constants import tilesize_x, tilesize_y

    global headcoord
    global tail

    # draw head
    headcoord_px = pixelcoord_in_playfield(headcoord)
    headcoord_x, headcoord_y = headcoord_px
    pygame.draw.rect(
        surf,
        snakeheadcolor,
        pygame.Rect(headcoord_x, headcoord_y, tilesize_x, tilesize_y),
    )

    # draw tail
    for tailcoord in tail:
        tailcoord_x, tailcoord_y = pixelcoord_in_playfield(tailcoord)
        pygame.draw.rect(
            surf,
            snaketailcolor,
            pygame.Rect(tailcoord_x, tailcoord_y, tilesize_x, tilesize_y),
        )
