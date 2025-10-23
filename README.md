# Minesweeper (Pygame)

A faithful recreation of the classic Windows Minesweeper game, built with Python and Pygame. Features authentic Windows 95 styling with a manually-drawn smiley face button, proper flag markers, and original game mechanics.

## Features

✨ **Complete Gameplay**
- Classic Minesweeper rules: reveal cells, flag mines, win by revealing all safe cells
- "First-click safe" guarantee: mines are never placed on your first click
- Three difficulty levels: Beginner, Intermediate, Expert (selectable from menu)
- Auto-flag remaining mines on victory
- Real-time mine counter and timer

🎨 **Authentic UI**
- **Difficulty Selection Menu**: Graphical menu to choose game difficulty at startup
- Windows 95-style 3D beveled header with inset effects
- Grid-pattern background for visual depth
- Manually-drawn yellow smiley face that changes expression:
  - 😊 Normal (happy smile)
  - 😞 Lost (sad frown)
  - 😎 Won (cool sunglasses)
- Clickable smiley to restart the game
- Red mine count display (3-digit format)
- Red timer display (3-digit format)
- Proper flag markers (red flag graphics, not colored rectangles)
- Text with semi-transparent white background for readability

🎮 **Controls**
- **Left-click**: Reveal a cell
- **Right-click**: Place/remove flag
- **Click Smiley**: Restart game (also available from menu on difficulty selection)

## Quick Start

### Option 1: Standalone Executable (No Python Required)
Download and run `Minesweeper.exe` directly from the `dist/` folder. No dependencies needed!

```powershell
.\dist\Minesweeper.exe
```

### Option 2: Run from Source (Python Required)

```powershell
# Clone or navigate to the repo
cd C:\path\to\mswp

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt

# Run the game
python main.py
```

## Project Structure

```
.
├── main.py                  # Game class, DifficultyMenu, and main loop
├── board.py                 # Board generation, mine placement, reveal logic
├── cell.py                  # Cell state (covered, revealed, flagged, mine)
├── config.py                # Configuration constants (sizes, colors, difficulties)
├── generate_background.py   # Script to generate grid background image
├── requirements.txt         # Python dependencies (pygame)
├── SPEC.md                  # Game specification and requirements
├── README.md                # This file
├── images/                  # Asset folder
│   └── background.png       # Grid pattern background for menu
└── dist/                    # Standalone executable
    └── Minesweeper.exe      # Ready-to-run Windows executable
```

## Dependencies

- **Pygame 2.6+**: Rendering and event handling
- **Python 3.7+**: Runtime (only for source builds)

Install via: `pip install -r requirements.txt`

## Game Rules

1. **First Click**: Always safe—mines are placed after your first click, never on that cell or its 8 neighbors.
2. **Reveal Cell**: Left-click to reveal a cell.
   - If it's a mine → Game Over (Lost)
   - If it's safe → Shows adjacent mine count (or blank if 0)
   - If blank (0 adjacent mines) → Auto-reveals all adjacent cells (flood fill)
3. **Flag Cell**: Right-click to mark/unmark a mine guess.
4. **Win Condition**: Reveal all non-mine cells. Remaining mines auto-flag and smiley shows sunglasses.
5. **Lose Condition**: Reveal a mine. Game over, smiley frowns, all mines revealed.

## Architecture Notes

- **Game Logic** (board.py, cell.py): Completely separate from rendering for testability
- **Rendering** (main.py): Handles all Pygame drawing and display updates
- **Configuration** (config.py): All sizes, colors, and difficulty settings in one place

## Development

### Run from Source
```powershell
python main.py
# Menu will appear to select difficulty
```

### Build Standalone EXE (requires PyInstaller)
```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "images;images" --name=Minesweeper main.py
# Output: dist/Minesweeper.exe
```

### Regenerate Background Image
```powershell
python generate_background.py
# Creates images/background.png with grid pattern
```

### Code Quality
- Docstrings on all classes and public methods
- Inline comments for complex logic
- Game state kept explicit (normal → lost/won)
- Follows PEP 8 style guidelines
- Modular architecture for easy testing

## Testing

Currently no automated tests, but the modular design allows for easy unit testing of game logic in isolation.

## License

Public Domain / MIT License

## History

**October 2025 - Final Release**:
- ✅ Complete Windows 95-style Minesweeper implementation
- ✅ Graphical difficulty selection menu
- ✅ Grid-pattern background with text isolation
- ✅ Smiley face with three expressions (smile/frown/sunglasses)
- ✅ Authentic flag markers and UI styling
- ✅ Standalone Windows executable (no Python required)
- ✅ Full source code with documentation
