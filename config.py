
"""UI and gameplay configuration constants.

Place project-wide constants that affect sizing, layout and default difficulties here.
"""

# Pixel size of a single cell square
CELL_SIZE = 24

# Height (in pixels) of the header area that shows mines/timer/smiley
HEADER_HEIGHT = 40

# Small margin used by UI elements (unused in minimal scaffold but left for extension)
MARGIN = 5

# Difficulty presets: (cols, rows, mines)
DIFFICULTIES = {
    'beginner': (9, 9, 10),
    'intermediate': (16, 16, 40),
    'expert': (30, 16, 99),
}

# Main loop frame-rate
FPS = 30
