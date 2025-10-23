"""
Generate a background image for the Minesweeper menu.
Creates a more visually interesting gradient background.
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

# Create a radial gradient background (center is lighter)
center_x, center_y = width // 2, height // 2
max_dist = ((width/2)**2 + (height/2)**2) ** 0.5

for y in range(height):
    for x in range(width):
        # Calculate distance from center
        dist = ((x - center_x)**2 + (y - center_y)**2) ** 0.5
        # Calculate color based on distance (160 to 100)
        gray_val = min(255, max(80, int(160 - (dist / max_dist) * 80)))
        surface.set_at((x, y), (gray_val, gray_val, gray_val))

# Add diagonal stripes for visual interest
for i in range(0, width + height, 20):
    pygame.draw.line(surface, (200, 200, 200), (i, 0), (i - height, height), 1)

# Add a checkered pattern overlay (very subtle)
for x in range(0, width, 40):
    for y in range(0, height, 40):
        pygame.draw.rect(surface, (190, 190, 190), (x, y, 20, 20), 1)

# Save the image
pygame.image.save(surface, 'images/background.png')
print("✓ Background image created: images/background.png (Radial gradient with pattern)")

pygame.quit()
