# Python code to fix the division by zero error and refine the tethering mechanic

import pygame
import sys

# Constants for simulation
GRAVITY = 0.5
ELASTICITY = 0.1  # Adjusted for smoother tethering

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
mouse_pos = (0, 0)

# Main loop
def main():
    global dragging, mouse_pos, box, box_velocity
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(event.pos):
                    dragging = True
                    mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        if dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            force_direction = (current_mouse_pos[0] - mouse_pos[0], current_mouse_pos[1] - mouse_pos[1])
            force_magnitude = (force_direction[0]**2 + force_direction[1]**2)**0.5
            # Prevent division by zero
            if force_magnitude != 0:
                normalized_force = (force_direction[0] / force_magnitude, force_direction[1] / force_magnitude)
                force = (normalized_force[0] * ELASTICITY, normalized_force[1] * ELASTICITY)
                box_velocity[0] += force[0]
                box_velocity[1] += force[1]
            mouse_pos = current_mouse_pos

        # Apply gravity
        box_velocity[1] += GRAVITY

        # Move the box
        box.x += int(box_velocity[0])
        box.y += int(box_velocity[1])

        # Boundary collision detection
        if box.left < 0 or box.right > 800:
            box_velocity[0] = -box_velocity[0]
        if box.top < 0 or box.bottom > 600:
            box_velocity[1] = -box_velocity[1]

        # Draw everything
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), box)

        # Update the display
        pygame.display.flip()

        # Tick
        clock.tick(60)

if __name__ == '__main__':
    main()
