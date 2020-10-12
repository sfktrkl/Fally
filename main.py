import pygame
import os

from Fally import *
from Wall import *

# Set window position to the right of the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1400, 50)

WIN_WIDTH = 500
WIN_HEIGHT = 1000

# TODO, Change this icon
ICON = pygame.image.load(os.path.join("imgs", "fally.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Initialize fonts to draw stats(scores)
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

# Update graphics
def draw_window(win, fally, walls, score):
    # win blit simply draws
    win.blit(BG_IMG, (0,0))
    fally.draw(win)
    for wall in walls:
        wall.draw(win)
    # Create a text to draw score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()

# Create main loop
def main():
    # Create Fally at the middle of the window
    fally = Fally(240, 100)
    # Create first wall at the bottom of window
    walls = [Wall(WIN_HEIGHT)]
    # Distance between walls
    d_walls = 400

    # Arrange game window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Fally")
    pygame.display.set_icon(ICON)

    # Creates a Clock that can be used to track an amount of time.
    clock = pygame.time.Clock()

    run = True
    score = 0
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

        for wall in walls:
            # If wall is passed but a collision exist, reduce score
            if not wall.passed and wall.collide(fally):
                wall.passed = True
                score -= 1
            # If wall is passed and no collision occured, increase score
            if not wall.passed and wall.y < fally.y:
                wall.passed = True
                score += 1
            # If wall gets outside the window, it needs to be deleted
            if wall.y + wall.IMG.get_width() < 0:
                walls.remove(wall)
            # If wall reaches close enough to Fally, another wall needs to be created
            # This way each wall will trigger creation of one another wall after itself.
            # So that, walls can always keep coming to Fally.
            if wall.needAnother and WIN_HEIGHT - (wall.y - fally.y) > d_walls:
                wall.needAnother = False
                walls.append(Wall(WIN_HEIGHT))
            wall.move()

        draw_window(win, fally, walls, score)

    pygame.quit()
    quit()

main()
