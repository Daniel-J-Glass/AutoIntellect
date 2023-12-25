# Water Simulation with Border Collision using Pygame

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Define the water particle class
class WaterParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        self.color = BLUE
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def move(self):
        # Update the particle's position
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Collision with borders
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.velocity[0] *= -1
        if self.y <= 0 or self.y >= SCREEN_HEIGHT:
            self.velocity[1] *= -1

    def draw(self, screen):
        # Draw the particle on the screen
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Water Simulation with Border Collision')

# Create a list to hold water particles
particles = [WaterParticle(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(100)]

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Update the screen
    screen.fill(WHITE)
    for particle in particles:
        particle.move()
        particle.draw(screen)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(10)

# If the script is run directly (and not imported), run the main loop
if __name__ == '__main__':
    main()