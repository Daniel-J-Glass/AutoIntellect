# Import necessary libraries
import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
BOX_COLOR = (255, 165, 0)
FRICTION = 0.99

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Box Rotation and Fling Simulation')

# Define a vector2 class to emulate Pygame's in environments that may lack Pygame
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        raise ValueError('Can only multiply by int or float')

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        len = self.length()
        if len > 0:
            self.x /= len
            self.y /= len
        return self

# Create a mock class with partial Pygame functionality for non-Pygame environments
if not hasattr(pygame, 'Vector2'):
    pygame.Vector2 = Vector2
    pygame.Rect = lambda x, y, w, h: (x, y, w, h)

# ... Rest of the code here ...

