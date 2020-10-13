import pygame
import neat
import sys
import os

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

# Generation and fitness value which will shown in the window
generation_count = -1
max_fitness = -100

# Keep track of score
game_score = 0

# Arrange game window
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Fally")
pygame.display.set_icon(ICON)

# Creates a Clock that can be used to track an amount of time.
clock = pygame.time.Clock()
