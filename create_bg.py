import pygame
import os

os.makedirs('images', exist_ok=True)
pygame.init()

# Create surface with radial gradient
surface = pygame.Surface((400, 400))
center_x, center_y = 200, 200
max_dist = ((200)**2 + (200)**2) ** 0.5

for y in range(400):
    for x in range(400):
        dist = ((x - center_x)**2 + (y - center_y)**2) ** 0.5
        gray_val = min(255, max(80, int(160 - (dist / max_dist) * 80)))
        surface.set_at((x, y), (gray_val, gray_val, gray_val))

# Add diagonal lines
for i in range(0, 800, 20):
    pygame.draw.line(surface, (200, 200, 200), (i, 0), (i - 400, 400), 1)

pygame.image.save(surface, 'images/background.png')
print("✓ Background created!")
pygame.quit()
