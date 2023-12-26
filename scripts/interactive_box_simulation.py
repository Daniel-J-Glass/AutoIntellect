import pygame
import sys

# Constants for simulation
GRAVITY = 0.5
ELASTICITY = 0.05
MAX_FORCE = 10  # Maximum force applied by the tether to prevent exponential increase

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Define the box
box = pygame.Rect(350, 250, 100, 100)
box_velocity = [0, 0]

# Variables for dragging and tethering
dragging = False
pivot = None

def main():
    global dragging, pivot, box, box_velocity
    # Main loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(event.pos):
                    dragging = True
                    pivot = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                pivot = None

        # Apply gravity
        box_velocity[1] += GRAVITY

        # Move the box
        box.x += box_velocity[0]
        box.y += box_velocity[1]

        # Apply tethering force if dragging
        if dragging and pivot:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            force_x = (mouse_x - pivot[0]) * ELASTICITY
            force_y = (mouse_y - pivot[1]) * ELASTICITY
            # Limit the force to prevent exponential increase
            force_x = min(force_x, MAX_FORCE)
            force_y = min(force_y, MAX_FORCE)
            box_velocity[0] += force_x
            box_velocity[1] += force_y

        # Collision detection with the floor
        if box.bottom > 600:
            box.bottom = 600
            box_velocity[1] = -box_velocity[1] * 0.9  # Apply some damping

        # Draw everything
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), box)

        # Update the display
        pygame.display.flip()

        # Tick
        clock.tick(60)

if __name__ == '__main__':
    main()
