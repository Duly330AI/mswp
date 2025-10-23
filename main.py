"""Main game module.

Contains the Game class which encapsulates Minesweeper's state and
behavior (event handling, rendering and main loop). The `run` function is
a small wrapper around `Game.run()` for script entry.
"""

import pygame
from config import CELL_SIZE, HEADER_HEIGHT, FPS
from config import DIFFICULTIES
from board import Board


class Game:
    """Encapsulates Minesweeper game state and behavior.

    Public methods:
      - reset_game(): reinitialize the board and timer
      - handle_events(): poll and handle pygame events
      - draw(): render header and grid
      - run(): start the main loop
    """

    def __init__(self, difficulty='beginner'):
        pygame.init()
        self.difficulty = difficulty
        self.cols, self.rows, self.mines = DIFFICULTIES.get(difficulty, DIFFICULTIES['beginner'])
        self.width = self.cols * CELL_SIZE
        self.height = HEADER_HEIGHT + self.rows * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Minesweeper (minimal)')
        self.clock = pygame.time.Clock()

        # game state
        self.board = None
        self.running = True
        self.game_over = False
        self.smiley_state = 'normal'  # normal, lost, won

        # timer
        self.timer_start = None
        self.elapsed_seconds = 0

        # smiley rect
        self.smiley_rect = pygame.Rect(self.width//2 - 16, 4, 32, HEADER_HEIGHT-8)

        self.reset_game()

    def reset_game(self):
        """Reset the game state to a fresh board with the same difficulty.

        This method re-initializes the board, clears the timer and resets
        the UI state so a new game can begin.
        """
        self.board = Board(self.cols, self.rows, self.mines)
        self.running = True
        self.game_over = False
        # use simple string states for smiley drawing: 'normal', 'lost', 'won'
        self.smiley_state = 'normal'
        self.timer_start = None
        self.elapsed_seconds = 0

    def handle_events(self):
        """Process pending Pygame events (input/action handling)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # smiley click restarts even if game over
                if event.button == 1 and self.smiley_rect.collidepoint(mx, my):
                    self.reset_game()
                    return
                # ignore other clicks when game is over
                if self.game_over:
                    return
                # only respond to clicks on the grid area
                if my >= HEADER_HEIGHT:
                    gx = mx // CELL_SIZE
                    gy = (my - HEADER_HEIGHT) // CELL_SIZE
                    if event.button == 1:
                        # left click: possibly place mines and reveal
                        if not self.board.mines_placed:
                            self.board.place_mines(gx, gy)
                            self.timer_start = pygame.time.get_ticks()
                        cell = self.board.grid[gy][gx]
                        self.board.reveal(gx, gy)
                        if cell.mine:
                            # loss
                            cell.exploded = True
                            self.board.reveal_all_mines()
                            self.game_over = True
                            # set state for lost (will affect drawn smiley)
                            self.smiley_state = 'lost'
                        else:
                            # check for win after reveal
                            if self.board.check_win():
                                self.game_over = True
                                # set state for won (will affect drawn smiley)
                                self.smiley_state = 'won'
                                # auto-flag remaining mines for clarity
                                for yy in range(self.board.height):
                                    for xx in range(self.board.width):
                                        c = self.board.grid[yy][xx]
                                        if c.mine:
                                            c.flagged = True
                    elif event.button == 3:
                        # right click: toggle a flag
                        cell = self.board.grid[gy][gx]
                        cell.toggle_flag()

    def draw(self):
        """Render the header and the grid to the screen."""
        # clear background
        self.screen.fill((200,200,200))
        # header
        pygame.draw.rect(self.screen, (100,100,100), (0,0,self.width,HEADER_HEIGHT))
        font = pygame.font.SysFont(None, 28)
        remaining = max(0, self.board.mines - self.board.flagged_count)
        mines_txt = font.render(f"Mines: {remaining}", True, (255,0,0))
        self.screen.blit(mines_txt, (8, 8))

        # update timer
        if self.timer_start is not None and not self.game_over:
            self.elapsed_seconds = int((pygame.time.get_ticks() - self.timer_start) / 1000)

        # draw smiley manually inside self.smiley_rect
        sx, sy, sw, sh = self.smiley_rect
        cx = sx + sw // 2
        cy = sy + sh // 2
        # make the smiley smaller so it doesn't overlap header text
        radius = int(min(sw, sh) * 0.28)

        # determine which state to display. If mines aren't placed yet show 'normal'.
        exploded_exists = any(
            self.board.grid[yy][xx].exploded
            for yy in range(self.board.height)
            for xx in range(self.board.width)
        )
        if not self.board.mines_placed:
            display_state = 'normal'
        elif exploded_exists:
            display_state = 'lost'
        else:
            display_state = self.smiley_state

        # face (yellow circle)
        pygame.draw.circle(self.screen, (255, 215, 0), (cx, cy), radius)

        # eyes positions
        eye_dx = max(1, radius // 2)
        eye_dy = -max(1, radius // 6)
        eye_r = max(2, radius // 6)
        left_eye = (cx - eye_dx, cy + eye_dy)
        right_eye = (cx + eye_dx, cy + eye_dy)

        # draw eyes or sunglasses for 'won'
        if display_state == 'won':
            rect_w = max(4, eye_r * 2)
            rect_h = max(2, eye_r)
            pygame.draw.rect(self.screen, (0,0,0), (left_eye[0]-rect_w//2, left_eye[1]-rect_h//2, rect_w, rect_h))
            pygame.draw.rect(self.screen, (0,0,0), (right_eye[0]-rect_w//2, right_eye[1]-rect_h//2, rect_w, rect_h))
        else:
            pygame.draw.circle(self.screen, (0,0,0), left_eye, eye_r)
            pygame.draw.circle(self.screen, (0,0,0), right_eye, eye_r)

        # mouth geometry
        mouth_w = max(6, radius)
        mouth_h = max(2, radius // 4)
        mouth_y = cy + radius // 3

        # Draw mouth: normal -> smile, lost -> frown, won -> straight line
        if display_state == 'normal':
            for i in range(-mouth_w//2, mouth_w//2):
                x1 = cx + i
                rel = (i / (mouth_w/2))
                y_off = int((1 - rel*rel) * mouth_h)
                pygame.draw.line(self.screen, (0,0,0), (x1, mouth_y + y_off), (x1, mouth_y + y_off))
        elif display_state == 'lost':
            for i in range(-mouth_w//2, mouth_w//2):
                x1 = cx + i
                rel = (i / (mouth_w/2))
                y_off = int(- (1 - rel*rel) * mouth_h)
                pygame.draw.line(self.screen, (0,0,0), (x1, mouth_y + y_off), (x1, mouth_y + y_off))
        else:
            pygame.draw.line(self.screen, (0,0,0), (cx - mouth_w//2, mouth_y), (cx + mouth_w//2, mouth_y), 2)

        timer_txt = font.render(f"Time: {self.elapsed_seconds}", True, (255,255,255))
        self.screen.blit(timer_txt, (self.width - timer_txt.get_width() - 8, 8))

        # grid
        for y in range(self.board.height):
            for x in range(self.board.width):
                rect = pygame.Rect(x*CELL_SIZE, HEADER_HEIGHT + y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell = self.board.grid[y][x]
                color = (180,180,180) if not cell.revealed else (220,220,220)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)
                if cell.flagged and not cell.revealed:
                    # draw a flag: vertical pole and triangular flag
                    pole_x = rect.centerx - 2
                    pole_y = rect.top + 4
                    pole_h = rect.height - 8
                    pygame.draw.line(self.screen, (0, 0, 0), (pole_x, pole_y), (pole_x, pole_y + pole_h), 2)
                    # flag triangle (red)
                    flag_w = 8
                    flag_h = 6
                    flag_points = [
                        (pole_x + 2, pole_y),
                        (pole_x + 2 + flag_w, pole_y + flag_h // 2),
                        (pole_x + 2, pole_y + flag_h)
                    ]
                    pygame.draw.polygon(self.screen, (200, 0, 0), flag_points)
                if cell.revealed and cell.mine:
                    if cell.exploded:
                        pygame.draw.rect(self.screen, (200,50,50), rect)
                    cx = rect.x + rect.width//2
                    cy = rect.y + rect.height//2
                    radius = rect.width//2 - 4
                    pygame.draw.circle(self.screen, (0,0,0), (cx, cy), radius)
                if cell.revealed and cell.adjacent > 0:
                    num_font = pygame.font.SysFont(None, 18)
                    txt = num_font.render(str(cell.adjacent), True, (0,0,0))
                    self.screen.blit(txt, (rect.x+4, rect.y+2))

        pygame.display.flip()

    def run(self):
        """Main loop: handle events, draw frame, and cap FPS."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


def run(difficulty='beginner'):
    Game(difficulty).run()


if __name__ == '__main__':
    run()
