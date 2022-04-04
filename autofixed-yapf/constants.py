# holds all constants for the snake game

from typing import Tuple
# max iterations of the main loop per second
FPS_max = 30

# number of moves per second
moves_per_second = 10.0
ticks_per_move = int(FPS_max / moves_per_second)

# playfield size: tiles in x- and y-direction
playfieldsize_x = 20
playfieldsize_y = 20
playfieldsize = (playfieldsize_x, playfieldsize_y)

# window size in pixels: x- and y-direction
screensize_x = 500
screensize_y = 500
screensize = (screensize_x, screensize_y)

# background color in rgb
backgroundcolor = (210,210,210) # light grey

# snake color (head/tail)
snakeheadcolor = (215,48,31) # orange
snaketailcolor = (252,141,89)  # pale orange

# meal color
mealcolor = (44,162,95) # dark green

# size of the playfield in px. Should not differ from screensize unless an indicator for
# the playable area is added.
playfield_width_px = 500
playfield_height_px = 500
playfieldsize_px = (playfield_width_px, playfield_height_px)

#### do not change
tilesize_x = int(playfield_width_px / playfieldsize_x)
tilesize_y = int(playfield_height_px / playfieldsize_y)

# playfield coordinates go from (0,0) to (playfield_size_x-1, playfield_size_y-1).
def pixelcoord_in_playfield(playfield_coords: Tuple[int]):
    """Takes playfield-coordinate (x,y), returns pixel coord of the
    top-left corner of that position in the playfield."""

    playfield_x, playfield_y = playfield_coords
    px_x = tilesize_x * playfield_x
    px_y = tilesize_y * playfield_y
    return (px_x, px_y)

#### do change