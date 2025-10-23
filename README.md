# Minesweeper (Pygame)

A faithful recreation of the classic Windows Minesweeper game, built with Python and Pygame. Features authentic Windows 95 styling with a manually-drawn smiley face button, proper flag markers, and original game mechanics.

## Features

✨ **Complete Gameplay**
- Classic Minesweeper rules: reveal cells, flag mines, win by revealing all safe cells
- "First-click safe" guarantee: mines are never placed on your first click
- Three difficulty levels: Beginner, Intermediate, Expert
- Auto-flag remaining mines on victory
- Real-time mine counter and timer

🎨 **Authentic UI**
- Windows 95-style 3D beveled header with inset effects
- Manually-drawn yellow smiley face that changes expression:
  - 😊 Normal (happy smile)
  - 😞 Lost (sad frown)
  - 😎 Won (cool sunglasses)
- Clickable smiley to restart the game
- Red mine count display (3-digit format)
- Red timer display (3-digit format)
- Proper flag markers (not just colored rectangles)

🎮 **Controls**
- **Left-click**: Reveal a cell
- **Right-click**: Place/remove flag
- **Click Smiley**: Restart game

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
├── main.py              # Game class and main loop
├── board.py             # Board generation, mine placement, reveal logic
├── cell.py              # Cell state (covered, revealed, flagged, mine)
├── config.py            # Configuration constants (sizes, colors, difficulties)
├── requirements.txt     # Python dependencies (pygame)
├── SPEC.md              # Game specification and rules
├── dist/                # Standalone executable (Minesweeper.exe)
└── README.md            # This file
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
```

### Build Standalone EXE (requires PyInstaller)
```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name=Minesweeper main.py
# Output: dist/Minesweeper.exe
```

### Code Quality
- Docstrings on all classes and public methods
- Inline comments for complex logic
- Game state kept explicit (normal → lost/won)
- Follows PEP 8 style guidelines

## Testing

Currently no automated tests, but the modular design allows for easy unit testing of game logic in isolation.

## License

Public Domain / MIT License

## History

**October 2025**: Complete implementation with Windows 95 UI styling, smiley face button, flag markers, and standalone executable.
