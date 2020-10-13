from Fally import *
from Wall import *
from Settings import *

# Update graphics
def draw_window(fallies, walls, genomes):
    # win blit simply draws
    win.blit(BG_IMG, (0,0))

    # Draw each fally
    for fally in fallies:
        fally.draw(win)

    # Draw each wall
    for wall in walls:
        wall.draw(win)

    # Draw a text which will show generations
    generation_label = STAT_FONT.render("Generation: " + str(generation_count), 1, (255, 0, 0))
    win.blit(generation_label, (10, 10))

    # Find the maximum fitness value from individuals
    global max_fitness
    if len(genomes) > 0:
        fitnesses = []
        for genome in genomes:
            fitnesses.append(genome.fitness)
        max_fitness = max(fitnesses)

   # Draw a text which will show maximum fitness
    fitness_label = STAT_FONT.render("Fitness: " + str(max_fitness), 1, (255, 0, 0))
    win.blit(fitness_label, (10, 50))

    # Draw a text which will show number of alive Fallies
    alive_label = STAT_FONT.render("Alive: " + str(len(fallies)), 1, (255, 0, 0))
    win.blit(alive_label, (10, 100))

    pygame.display.update()

# Fitness function for AI
def fitness(neat_genomes, config):

    # Keep track of generation count to show in window
    global generation_count
    generation_count += 1

    # Create lists which contains the genomes, associated
    # neural network and Fally which contains these objects
    # in same order.
    neural_networks = []
    genomes = []
    fallies = []
    for genome_id, genome in neat_genomes:
        genome.fitness = 0  # start with fitness level of 0
        neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_networks.append(neural_network)
        fallies.append(Fally(240, 100))
        genomes.append(genome)

    # Create first wall at the bottom of window
    walls = [Wall(400)]
    # Distance between walls
    d_walls = 300

    while len(fallies) > 0:
        # Limit the runtime speed of the game.
        # So, it will never run at more than 60 fps.
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Stop AI by reaching treshold fitness
                    # TODO Find another way to stop
                    genomes[0].fitness = 100
                    return

        # Find closest wall to fallies.
        # So, this wall can be used to give inputs
        # to neural networks.
        wall_index = 0
        min_y = WIN_HEIGHT
        if len(fallies) > 0:
            for x, wall in enumerate(walls):
                if wall.y < min_y and fallies[0].y < wall.y:
                    wall_index = x
                    min_y = wall.y

        # Move fallies according to output taken from neural networks
        for x, fally in enumerate(fallies):
            fally.move()

            #                           left                  right            #
            # ----------------------------|                     |------------- #
            #                             |                     |              #
            # ----------------------------|                     |------------- #
            # wall.left         wall.left + wall width      wall.right
            left = walls[wall_index].left + walls[wall_index].IMG.get_width()
            right = walls[wall_index].right

            # Inputs: Fally.x, distance between left wall to Fally and distance between right wall to Fally
            output = neural_networks[x].activate((fally.x, abs(fally.x - left), abs(fally.x - right)))
            # Outputs: Move right or move left
            if output[0] > 0:
                fally.move_right()
            if output[0] < 0:
                fally.move_left()

        for wall in walls:
            wall.move()
            for fally in fallies:
                fally_index = fallies.index(fally)
                # If a collision is exist, reduce fitness and remove the Fally
                if wall.collide(fally):
                    genomes[fally_index].fitness -= 1
                    neural_networks.pop(fally_index)
                    genomes.pop(fally_index)
                    fallies.pop(fally_index)
                # If wall is passed and no collision occured, increase fitness
                elif wall.y < fally.y:
                    genomes[fally_index].fitness += 1
                    wall.passed = True

            # Check window height to create another wall.
            # Each wall will trigger creation of one another wall after itself.
            # So that, walls can always keep coming to Fally.
            if wall.needAnother and wall.y + d_walls < WIN_HEIGHT:
                wall.needAnother = False
                walls.append(Wall(wall.y + d_walls))

            # If wall is passed, delete it
            if wall.passed:
                walls.remove(wall)

        draw_window(fallies, walls, genomes)

def run_ai(config_path):
    # Get the configurations from file
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path)

    # Get population configuration
    p = neat.Population(config)

    # This will give some stats to console
    stats = neat.StatisticsReporter()
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(stats)

    # Reset generation count and max fitness
    global generation_count
    global max_fitness
    generation_count = -1
    max_fitness = -100

    # Set the fitness function for at most 10 generations
    p.run(fitness, 10)
