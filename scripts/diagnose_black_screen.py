
import pygame
import sys

# Pygame initialization
pygame.init()

# Set the WIDTH and HEIGHT of the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption('Interactive Box Simulation')

# Run until the user asks to quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
