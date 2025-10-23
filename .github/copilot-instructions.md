<!-- .github/copilot-instructions.md for Minesweeper (Pygame) -->

# Repository guidance for AI coding agents

This repository is a small Python desktop game (Minesweeper) built with Pygame. Use these notes to be productive quickly — focus on the concrete files and patterns used here.

1. Big-picture architecture (what to edit)
   - `main.py` — game loop, event handling, window setup. Changes here affect startup, input handling and overall flow.
   - `board.py` — board generation, mine placement rules, reveal/propagation logic. Core game rules live here.
   - `cell.py` — per-cell state (covered/flagged/mine/count). Small, well-defined data object logic resides here.
   - `config.py` — constants (colors, sizes, difficulty presets). Use for any UI or size changes.
   - `SPEC.md` — canonical project spec and requirements (use for behavioral checks such as "first click safe").

2. Key project-specific rules and patterns
   - Mines are placed only after the first click and must avoid the 3x3 area around the initial click (see `SPEC.md`). Look for placement logic in `board.py`.
   - UI sizing adapts to grid size (window dimensions depend on cell size * grid). Prefer updating `config.py` over hardcoding sizes.
   - State transitions are explicit: covered -> revealed, flagged toggles. Tests and changes should respect these state machines in `cell.py` and `board.py`.

3. Build / run / debug
   - No build step. Run locally with the project's Python environment.
   - Primary run command: `python main.py` (from repository root). If using `pwsh`/PowerShell, run the same command.
   - There are no tests present. When adding tests, keep them lightweight and decoupled from Pygame rendering (extract logic to non-graphical functions in `board.py`/`cell.py`).

4. Conventions and style to follow in edits
   - Keep game logic (deterministic rules) separate from rendering. If a change mixes both, suggest refactoring to move logic into `board.py`/`cell.py` so it can be tested.
   - Use constants from `config.py` for UI values (colors, cell size, header height). If you add a new visual constant, put it in `config.py`.
   - Preserve the "first-click-safe" contract in all board generation changes.

5. Integration points & external dependencies
   - External dependency: Pygame. Any change that affects event loop timing or surfaces must consider Pygame APIs.
   - No network, DB, or external services are used.

6. Examples (where to look for patterns)
   - If you need to change mine placement, open `board.py` and find the function that runs after the first click; follow existing variable names (e.g. `place_mines`, `reveal`) to keep consistency.
   - To change header layout (mines/timer/smiley), update sizes in `config.py` and adjust `main.py` rendering order.

7. Safety checks an agent should perform before editing
   - Run the game manually (`python main.py`) to verify no immediate runtime errors after edits.
   - For logic-only changes, add a small Python unit test (pytest/unittest) that imports `board.py` and validates board generation (first-click-safe and correct mine count).

8. What NOT to change without human approval
   - The expected gameplay rules in `SPEC.md` (difficulty sizes/counts and first-click-safe behaviour).
   - Any user-facing coordinate math that affects rendering without updating dependent UI constants.

9. If you add tests or CI
   - Tests should avoid launching Pygame windows. Extract logic into pure-Python functions and test those.

If something in this file is unclear or you need more repo specifics (for example the exact function names in `board.py`), ask and I'll open the file(s) and update the instructions with precise code pointers.
