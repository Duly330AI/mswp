"""
Generate a background image for the Minesweeper menu.
Creates a gradient background with a subtle pattern.
"""

import pygame
import os

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Initialize pygame
pygame.init()

# Create a 400x400 surface
width, height = 400, 400
surface = pygame.Surface((width, height))

# Create a gradient background (top to bottom, darker gray to lighter gray)
for y in range(height):
    # Calculate color intensity based on y position (160 to 200)
    gray_val = min(255, max(0, 160 + int((y / height) * 40)))
    pygame.draw.line(surface, (gray_val, gray_val, gray_val), (0, y), (width, y), 1)

# Add a subtle diamond pattern overlay
pygame.draw.line(surface, (200, 200, 200), (0, 0), (width, height), 1)
pygame.draw.line(surface, (200, 200, 200), (width, 0), (0, height), 1)

# Add some subtle circles for visual interest
for x in range(0, width, 100):
    for y in range(0, height, 100):
        pygame.draw.circle(surface, (180, 180, 180), (x, y), 30, 1)

# Save the image
pygame.image.save(surface, 'images/background.png')
print("✓ Background image created: images/background.png")

pygame.quit()
