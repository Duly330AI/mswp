from dataclasses import dataclass


@dataclass
class Cell:
    """Represents one cell on the Minesweeper board.

    Attributes:
        x (int): column index
        y (int): row index
        mine (bool): True if this cell contains a mine
        revealed (bool): True if the cell has been revealed to the player
        flagged (bool): True if the player has placed a flag on this cell
        exploded (bool): True if this mine was the one that triggered a loss
        adjacent (int): number of adjacent mines
    """
    x: int
    y: int
    mine: bool = False
    revealed: bool = False
    flagged: bool = False
    exploded: bool = False
    adjacent: int = 0

    def reveal(self):
        """Reveal this cell (mark it as visible)."""
        self.revealed = True

    def toggle_flag(self):
        """Toggle a flag on this cell.

        Flags can only be toggled on covered (not revealed) cells.
        """
        if not self.revealed:
            self.flagged = not self.flagged
