from Fally import *
from Wall import *
from Settings import *
from AI import *
from Game import *

# Create main loop
def menu():

    # Initial colors of the buttons
    play_label_color = (255, 0, 0)
    ai_label_color = (255, 0, 0)

    while True:
        # Limit the runtime speed of the game.
        # So, it will never run at more than 60 fps.
        clock.tick(60)

        # Draw background
        win.blit(BG_IMG, (0,0))

        # Create a text for PLAY GAME
        play_label = STAT_FONT.render("PLAY GAME", 1, play_label_color)
        play_label_x = int((WIN_WIDTH - play_label.get_width()) / 2)
        play_label_y = int(WIN_HEIGHT / 2 - 150)
        play_label_rect = play_label.get_rect(topleft=(play_label_x, play_label_y))
        win.blit(play_label, (play_label_x, play_label_y))

        # Create text for AI
        ai_label = STAT_FONT.render("LET AI PLAYS", 1, ai_label_color)
        ai_label_x = int((WIN_WIDTH - ai_label.get_width()) / 2)
        ai_label_y = int(WIN_HEIGHT / 2 - 100)
        ai_label_rect = ai_label.get_rect(topleft=(ai_label_x, ai_label_y))
        win.blit(ai_label, (ai_label_x, ai_label_y))

        # Update graphics
        pygame.display.update()

        # Get mouse positon and if mouse hits one of the texts
        # update their colors
        mouse = pygame.mouse.get_pos()
        if play_label_rect.collidepoint((mouse[0], mouse[1])):
            play_label_color = (0, 255, 0)
            ai_label_color = (255, 0, 0)
        elif ai_label_rect.collidepoint((mouse[0], mouse[1])):
            play_label_color = (255, 0, 0)
            ai_label_color = (0, 255, 0)
        else:
            play_label_color = (255, 0, 0)
            ai_label_color = (255, 0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Use event.pos or pg.mouse.get_pos().
                    if play_label_rect.collidepoint(event.pos):
                        return "play_game"
                    elif ai_label_rect.collidepoint(event.pos):
                        return "run_ai"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play_game"
                elif event.key == pygame.K_ESCAPE:
                    return ""

def main():
    value = menu()
    # Run the game
    if value == "play_game":
        play_game()
    # Run AI
    elif value == "run_ai":
        run_ai(config_path)
    # Call this method recursively.
    # This way game will never end.
    main()

# This will give the path to the directory that we are in
# So, configuration file for NEAT can be loaded.
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    main()
