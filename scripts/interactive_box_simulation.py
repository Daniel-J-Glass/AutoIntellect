import pygame
import sys

# Define the pygame initialization function

def init_pygame():
    pygame.init()
    # Define the display resolution
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Interactive Box Simulation with Mouse Interaction')
    return screen

# Define main loop

def run_simulation(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        # Update the screen with whatever changes have been made
        pygame.display.flip()
        clock.tick(60)

# Execute the simulation
if __name__ == '__main__':
    screen = init_pygame()
    run_simulation(screen)