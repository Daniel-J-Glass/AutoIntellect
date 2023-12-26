import pygame

# Define a function to rotate the box
def rotate_box(angle, rotation_speed):
    """Rotate the box by a given angle.

    Args:
        angle (float): The current angle of the box.
        rotation_speed (float): The speed at which the box should rotate.

    Returns:
        float: The new angle after rotation.
    """
    new_angle = (angle + rotation_speed) % 360
    return new_angle

# Main function to test the rotation mechanic
if __name__ == '__main__':
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Rotation Mechanic Test')

    # Set the initial angle and rotation speed
    angle = 0
    rotation_speed = 5

    # Load the box image
    box_image = pygame.Surface((100, 100))
    box_image.fill((255, 0, 0))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rotate the box
        angle = rotate_box(angle, rotation_speed)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Create a new surface with the specified angle
        rotated_box = pygame.transform.rotate(box_image, angle)
        box_rect = rotated_box.get_rect()
        box_rect.center = (400, 300)

        # Draw the rotated box
        screen.blit(rotated_box, box_rect.topleft)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    pygame.quit()