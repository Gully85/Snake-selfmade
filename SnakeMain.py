# main file, run this to run the program

# use the pygame module
import pygame
from automaticSnake import CL_move

pygame.init()

import constants

FPS_max = constants.FPS_max

import snake, meal

# limits the number of iterations per second. Call FrameLimiter.tick(fps: int) to wait
# until the last call is 1/fps seconds ago
FrameLimiter = pygame.time.Clock()


def main():
    screensize_px = constants.screensize
    screen = pygame.display.set_mode(screensize_px)

    background = pygame.Surface(screensize_px)
    background.convert()
    background.fill(constants.backgroundcolor)

    # move background to the screen. Sizes are already matching
    screen.blit(background, (0, 0))

    # reveal
    pygame.display.flip()

    # main Event Loop
    while True:
        # limit execution speed
        FrameLimiter.tick(constants.FPS_max)

        process_user_input()

        # automatic mode, played by automaticSnake module. Comment this block
        # to let the user play
        import automaticSnake

        if automaticSnake.LC_path_is_free():
            snake.set_direction(automaticSnake.LC_move())
        elif automaticSnake.CL_path_is_free():
            snake.set_direction(automaticSnake.CL_move())
        # TODO more fall-back strategies here. Currently, if CL and LC strategies are blocked, this will
        # just move forward until one becomes unblocked or the game is lost

        if snake.get_pause_state():
            continue

        # proceed in-game time
        snake.tick()
        # check for game-end
        if not snake.check_alive():
            print("Final score:", snake.getlength())
            exit()

        # draw new state
        screen.blit(background, (0, 0))
        snake.draw(screen)
        meal.draw(screen)
        pygame.display.flip()


def process_user_input():
    """Looks through the event-Queue, hands accepted
    inputs (left/right/up/down/p) over to the snake module"""
    from pygame.locals import (
        QUIT,
        KEYDOWN,
        K_LEFT,
        K_RIGHT,
        K_UP,
        K_DOWN,
        K_ESCAPE,
        K_p,
    )

    # pygame has an event-queue, all inputs are KEYDOWN events in that.
    for event in pygame.event.get():

        # end process when game window is closed
        if event.type == QUIT:
            exit()

        # accepted user inputs: Esc left right top down P. Others are ignored.
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_LEFT:
                snake.set_direction("left")
            if event.key == K_RIGHT:
                snake.set_direction("right")
            if event.key == K_UP:
                snake.set_direction("up")
            if event.key == K_DOWN:
                snake.set_direction("down")
            if event.key == K_p:
                snake.toggle_pause()


# execute main if this is the file called, not just imported
if __name__ == "__main__":
    main()
