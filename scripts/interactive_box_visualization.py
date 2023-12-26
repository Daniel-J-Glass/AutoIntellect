import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Box Simulation')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the box class with rotation and fling mechanics
class Box:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.orientation = 0  # In degrees

    def rotate(self, angle):
        """Rotate the box by a given angle."""
        self.orientation = (self.orientation + angle) % 360

    def fling(self, force, angle):
        """Apply a force to the box in a given direction."""
        rad_angle = math.radians(angle)
        self.velocity[0] += force * math.cos(rad_angle)
        self.velocity[1] += force * math.sin(rad_angle)

    def draw(self, surface):
        # Calculate the box's new position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Draw the box
        box_rect = pygame.Rect(self.position[0], self.position[1], 50, 50)
        pygame.draw.rect(surface, WHITE, box_rect)

# Create a box instance
box = Box([width // 2, height // 2], [0, 0])

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill(BLACK)

    # Rotate and fling the box
    box.rotate(1)  # Rotate by 1 degree per frame
    box.fling(0.1, 90)  # Apply a small force upwards

    # Draw the box
    box.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()