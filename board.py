import random
from typing import List, Tuple
from cell import Cell


class Board:
    """Represents the game board and contains board-related logic.

    Responsibilities:
    - Maintain a grid of `Cell` objects
    - Place mines (after the first click) while honoring the "first-click-safe" rule
    - Compute adjacent mine counts
    - Reveal cells and propagate reveals for empty cells
    - Provide helpers for win/loss checks and flags
    """

    def __init__(self, width: int, height: int, mines: int):
        self.width = width
        self.height = height
        self.mines = mines
        # 2D grid y-major: grid[row][col]
        self.grid: List[List[Cell]] = [ [Cell(x,y) for x in range(width)] for y in range(height) ]
        self.mines_placed = False

    def in_bounds(self, x, y):
        """Return True if (x,y) is inside the board bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, x, y):
        """Yield neighbor Cell objects around (x,y) (8-way)."""
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                nx, ny = x+dx, y+dy
                if dx==0 and dy==0:
                    continue
                if self.in_bounds(nx, ny):
                    yield self.grid[ny][nx]

    def place_mines(self, safe_x: int, safe_y: int):
        """Place mines on the board after the first click.

        Mines are not placed until the first click to guarantee the initial click is safe.
        The 3x3 area around (safe_x, safe_y) is excluded from possible mine locations.
        This method is idempotent: calling it again after mines are placed is a no-op.
        """
        if self.mines_placed:
            return

        # Clear any previous mine markers (defensive) and reset adjacent counts
        for row in self.grid:
            for cell in row:
                cell.mine = False
                cell.adjacent = 0

        # Build candidate list excluding the 3x3 safe area
        candidates = []
        for y in range(self.height):
            for x in range(self.width):
                skip = False
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        if x == safe_x + dx and y == safe_y + dy:
                            skip = True
                            break
                    if skip:
                        break
                if not skip:
                    candidates.append((x,y))

        # Randomly select mine locations from candidates
        mines_to_place = min(self.mines, len(candidates))
        chosen = random.sample(candidates, mines_to_place)
        for x,y in chosen:
            self.grid[y][x].mine = True

        # Recompute adjacent mine counts for every cell
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                cell.adjacent = sum(1 for n in self.neighbors(x,y) if n.mine)

        self.mines_placed = True

    def reveal_all_mines(self):
        """Reveal all mines on the board (used when the player loses)."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.mine:
                    cell.revealed = True

    @property
    def flagged_count(self) -> int:
        """Return the number of flags currently set on the board."""
        return sum(1 for y in range(self.height) for x in range(self.width) if self.grid[y][x].flagged)

    def check_win(self) -> bool:
        """Return True when all non-mine cells have been revealed.

        This is used to detect a winning state after each reveal.
        """
        for y in range(self.height):
            for x in range(self.width):
                c = self.grid[y][x]
                if not c.mine and not c.revealed:
                    return False
        return True

    def reveal(self, x: int, y: int):
        """Reveal the cell at (x,y). If the cell is empty (adjacent==0), recursively reveal neighbors.

        Revealing is a no-op on already revealed or flagged cells.
        """
        cell = self.grid[y][x]
        if cell.revealed or cell.flagged:
            return
        cell.reveal()
        # propagate if no adjacent mines
        if cell.adjacent == 0 and not cell.mine:
            for n in self.neighbors(x,y):
                if not n.revealed:
                    self.reveal(n.x, n.y)
