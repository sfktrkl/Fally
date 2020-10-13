from Fally import *
from Wall import *
from Settings import *

# Create main loop
def game():
    # Reset score
    global game_score
    game_score = 0

    # Create Fally at the middle of the window
    fally = Fally(240, 100)
    # Create first wall at the bottom of window
    walls = [Wall(400)]
    # Distance between walls
    d_walls = 300

    while True:
        # Limit the runtime speed of the game.
        # So, it will never run at more than 60 fps.
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fally.move_left()
                elif event.key == pygame.K_RIGHT:
                    fally.move_right()
                elif event.key == pygame.K_ESCAPE:
                    return "menu"

        fally.move()

        for wall in walls:
            wall.move()

            # If wall is passed but a collision exist, reduce score
            if wall.collide(fally):
                wall.passed = True
                # Return to score window
                return "score"
            # If wall is passed and no collision occured, increase score
            elif wall.y < fally.y:
                wall.passed = True
                game_score += 1

            # Check window height to create another wall.
            # Each wall will trigger creation of one another wall after itself.
            # So that, walls can always keep coming to Fally.
            if wall.needAnother and wall.y + d_walls < WIN_HEIGHT:
                wall.needAnother = False
                walls.append(Wall(wall.y + d_walls))

            # If wall is passed, delete it
            if wall.passed:
                walls.remove(wall)

        # Draw background
        win.blit(BG_IMG, (0,0))

        # Draw Fally
        fally.draw(win)

        # Draw walls
        for wall in walls:
            wall.draw(win)

        # Create a text to draw score
        text = STAT_FONT.render("Score: " + str(game_score), 1, (255, 0, 0))
        win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

        # Update graphics
        pygame.display.update()

def score():
    while True:
        # Limit the runtime speed of the game.
        # So, it will never run at more than 60 fps.
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

        # Draw background
        win.blit(BG_IMG, (0,0))

        # Create a text for PLAY GAME
        score_label = STAT_FONT.render("Score: " + str(game_score), 1, (255, 0, 0))
        score_label_x = (WIN_WIDTH - score_label.get_width()) / 2
        score_label_y = WIN_HEIGHT / 2 - 150
        win.blit(score_label, (score_label_x, score_label_y))

        # Update graphics
        pygame.display.update()

def play_game():
    value = game()
    # Show score window
    if value == "score":
        if score():
            return
    # Show main menu
    elif value == "menu":
        return
