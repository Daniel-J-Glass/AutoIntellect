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

# Define the box class with rotation, fling mechanics, and collision detection
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

    def update(self):
        # Apply gravity
        self.velocity[1] += 0.5  # Gravity effect

        # Update the box's position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Collision detection with the floor
        if self.position[1] > height - 50:
            self.position[1] = height - 50
            self.velocity[1] = 0

    def draw(self, surface):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over the box
            if box_rect.collidepoint(event.pos):
                # Allow the user to drag the box
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            # Update the box position with the mouse
            box.position[0], box.position[1] = event.pos

    # Fill the screen with black
    screen.fill(BLACK)

    # Update the box
    box.update()

    # Draw the box
    box.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()