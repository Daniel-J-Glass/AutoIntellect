import pygame
import sys

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DICE_SIZE = 50
GRAVITY = 0.5
FRICTION = 0.1

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dice Rolling Simulation')

# Define dice class
class Dice:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.width = DICE_SIZE
        self.height = DICE_SIZE
        self.velocity = [0, 0]
        self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity[1] += GRAVITY

    def apply_friction(self):
        if self.on_ground:
            self.velocity[0] *= (1 - FRICTION)

    def update(self):
        self.apply_gravity()
        self.apply_friction()
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Collision detection with floor
        if self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity[1] = 0
            self.on_ground = True

        # Collision detection with ceiling
        if self.y <= 0:
            self.y = 0
            self.velocity[1] *= -0.5 # Add some bounce effect

        # Add side boundaries collision detection
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.velocity[0] *= -0.5 # Add some bounce effect

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height))

# Main function
def main():
    clock = pygame.time.Clock()
    dice = Dice()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Apply initial velocity based on mouse dragging
                # Removed random velocity to prevent dice from floating away
                dice.velocity = [5, -10]  # Example velocity

        # Update dice
        dice.update()

        # Drawing
        screen.fill((0, 0, 0))
        dice.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == '__main__':
    main()
