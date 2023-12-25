# Water simulation with particle collision dynamics

import pygame
import sys
from random import randint

# Constants
WIDTH, HEIGHT = 640, 480
PARTICLE_COLOR = (0, 105, 148)
PARTICLE_COUNT = 100
GRAVITY = (0, 0.5)

# Particle setup
class Particle:
    def __init__(self):
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)
        self.size = randint(1, 4)
        self.speed = [randint(-2, 2), randint(0, 5)]

    def move(self):
        self.speed[1] += GRAVITY[1]
        self.x += self.speed[0]
        self.y += self.speed[1]

    def bounce(self):
        if self.x <= 0 or self.x >= WIDTH:
            self.speed[0] = -self.speed[0]
        if self.y >= HEIGHT - self.size:
            self.speed[1] = -self.speed[1] * 0.9 # Some energy loss

    def draw(self, screen):
        pygame.draw.circle(screen, PARTICLE_COLOR, (int(self.x), int(self.y)), self.size)

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Water Simulation with Collisions')

# Main loop
particles = [Particle() for _ in range(PARTICLE_COUNT)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    for particle in particles:
        particle.move()
        particle.bounce()
        particle.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()