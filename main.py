import pygame
import os

from Fally import *

# Set window position to the right of the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400, 50)

WIN_WIDTH = 500
WIN_HEIGHT = 1000

# TODO, Change this icon
ICON = pygame.image.load(os.path.join("imgs", "fally.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Update graphics
def draw_window(win, fally):
    # win.blit simply draws
    win.blit(BG_IMG, (0,0))
    fally.draw(win)
    pygame.display.update()

# Create main loop
def main():
    fally = Fally(240, 100)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Fally")
    pygame.display.set_icon(ICON)

    # Creates a Clock that can be used to track an amount of time.
    clock = pygame.time.Clock()

    run = True
    while run:
        # Limit the runtime speed of the game.
        # So, it will never run at more than 60 fps.
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fally.move_left()
                elif event.key == pygame.K_RIGHT:
                    fally.move_right()

        fally.move()
        draw_window(win, fally)

    pygame.quit()
    quit()

main()
