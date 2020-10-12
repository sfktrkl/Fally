import pygame
import os

# Hero of our game, who is responsible for falling down :)
class Fally:
    MOVE_ACCELERATION = 1
    MOVE_SPEED = 3
    ROT_SPEED = 5        # How much it will rotate on each frame every time Fally moved

    # Load image for Fally
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "fally.png")))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0           # How much Fally will tilt while moving
        self.tick_count = 0     # Frame count, time passed after last move
        self.velocity = 0       # Movement velocity of Fally

    def move_right(self):
        # Prevent, Fally from getting out from right of the window
        # Since, WIN_WIDTH is 500, check position to less than this
        if self.x + self.IMG.get_width() < 500:
            self.velocity = self.MOVE_SPEED
            self.tick_count = 0

    def move_left(self):
        # Prevent, Fally from getting out from left of the window
        if self.x > 0:
            self.velocity = -self.MOVE_SPEED
            self.tick_count = 0

    def move(self):             # It will calculate how much Fally move in each frame
        self.tick_count += 1    # How many times we moved since last move

        # For each tick, distance traveled will reduce to zero slowly
        # Use the simple kinematic equation to calculate distance travel by Fally
        distance = 0
        if self.velocity > 0:
            distance = self.velocity * self.tick_count - 0.5 * self.MOVE_ACCELERATION * self.tick_count**2
            # When velocity of the Fally is positive avoid getting
            # negative distance values, to avoid start moving to other direction
            if distance < 0:
                distance = 0
        elif self.velocity < 0:
            distance = self.velocity * self.tick_count + 0.5 * self.MOVE_ACCELERATION * self.tick_count**2
            if distance > 0:
                distance = 0

        # Move Fally by amount of distance
        self.x = self.x + distance
        # Tilt Fally according to distance.
        # When it takes more distance, it will tilt more
        self.tilt = distance * -self.ROT_SPEED

    def draw(self, win):
        # Rotate image by the tilt amount
        rotated_image = pygame.transform.rotate(self.IMG, self.tilt)
        # Rotates image around its center
        new_rectangle = rotated_image.get_rect(center = self.IMG.get_rect(topleft = (self.x, self.y)).center)
        # win.blit simply draws
        win.blit(rotated_image, new_rectangle.topleft)

    # Used for per-pixel collision detection
    def get_mask(self):
        return pygame.mask.from_surface(self.IMG)
