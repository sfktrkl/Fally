import pygame
import os
import random

class Wall:
    SPEED = 5
    GAP = 100           # Gap between walls
    RANGE = 150         # Amount of change in the positions

    # Load image for wall
    IMG = pygame.image.load(os.path.join("imgs", "wall.png"))

    def __init__(self, y):
        self.y = y

        self.left = 0               # X position of the left wall
        self.right = 0              # X position of the right wall

        self.needAnother = True     # Is another wall is needed to drawn after this one
        self.passed = False         # Did Fally passed this wall, collision purposes
        self.set_position()

    def set_position(self):
        # Get a random position for left wall
        # Since wall has 300 width, wall should located outside the
        # window, (x position should be negative)
        self.left = random.randrange(-self.RANGE, 0)
        self.right = self.left + self.IMG.get_width() + self.GAP

    def move(self):
        # Move wall to up constantly
        self.y -= self.SPEED

    def draw(self, win):
        # Draw both left and right walls
        win.blit(self.IMG, (self.left, self.y))
        win.blit(self.IMG, (self.right, self.y))

    # Per-pixel collision detection
    def collide(self, fally):
        fally_mask = fally.get_mask()
        left_mask = pygame.mask.from_surface(self.IMG)
        right_mask = pygame.mask.from_surface(self.IMG)

        left_offset = (self.left - round(fally.x), self.y - fally.y)
        right_offset = (self.right - round(fally.x), self.y - fally.y)

        # overlap method will return none if no collision exists
        left_point = fally_mask.overlap(left_mask, left_offset)
        right_point = fally_mask.overlap(right_mask, right_offset)

        if (left_point or right_point):
            return True
        return False
