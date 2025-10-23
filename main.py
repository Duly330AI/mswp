"""Main game module.

Contains the Game class which encapsulates Minesweeper's state and
behavior (event handling, rendering and main loop). The DifficultyMenu class
displays a UI for selecting game difficulty before starting. The `run` function
is a small wrapper around `Game.run()` for script entry.
"""

import pygame
from config import CELL_SIZE, HEADER_HEIGHT, FPS
from config import DIFFICULTIES
from board import Board


class DifficultyMenu:
    """Displays a menu to select game difficulty before starting the game.
    
    Public methods:
      - run(): display the menu and return selected difficulty
    """
    
    def __init__(self):
        pygame.init()
        # menu window size
        self.width = 400
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Duly\'s Minesweeper - Select Difficulty')
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected_difficulty = None
        
        # button rectangles
        button_width = 150
        button_height = 50
        button_y_start = 140
        button_spacing = 70
        
        self.beginner_btn = pygame.Rect(self.width//2 - button_width//2, button_y_start, button_width, button_height)
        self.intermediate_btn = pygame.Rect(self.width//2 - button_width//2, button_y_start + button_spacing, button_width, button_height)
        self.expert_btn = pygame.Rect(self.width//2 - button_width//2, button_y_start + button_spacing*2, button_width, button_height)
    
    def handle_events(self):
        """Handle menu events (mouse clicks, window close)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if self.beginner_btn.collidepoint(mx, my):
                    self.selected_difficulty = 'beginner'
                    self.running = False
                elif self.intermediate_btn.collidepoint(mx, my):
                    self.selected_difficulty = 'intermediate'
                    self.running = False
                elif self.expert_btn.collidepoint(mx, my):
                    self.selected_difficulty = 'expert'
                    self.running = False
    
    def draw(self):
        """Render the difficulty menu."""
        self.screen.fill((192, 192, 192))
        
        # title
        font_title = pygame.font.SysFont(None, 32, bold=False)
        title = font_title.render("Duly's Minesweeper", True, (0, 0, 0))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 15))
        
        # subtitle
        font_subtitle = pygame.font.SysFont(None, 18)
        subtitle = font_subtitle.render("Schwierigkeitsstufe wählen", True, (50, 50, 50))
        self.screen.blit(subtitle, (self.width//2 - subtitle.get_width()//2, 50))
        
        # button font
        font_btn = pygame.font.SysFont(None, 20)
        
        # draw buttons
        buttons = [
            (self.beginner_btn, 'Beginner', (0, 150, 0)),
            (self.intermediate_btn, 'Intermediate', (200, 150, 0)),
            (self.expert_btn, 'Expert', (200, 0, 0))
        ]
        
        for btn_rect, label, color in buttons:
            # button background
            pygame.draw.rect(self.screen, color, btn_rect)
            # button border (3D effect)
            pygame.draw.line(self.screen, (255, 255, 255), btn_rect.topleft, btn_rect.topright, 2)
            pygame.draw.line(self.screen, (255, 255, 255), btn_rect.topleft, btn_rect.bottomleft, 2)
            pygame.draw.line(self.screen, (128, 128, 128), btn_rect.bottomleft, btn_rect.bottomright, 2)
            pygame.draw.line(self.screen, (128, 128, 128), btn_rect.topright, btn_rect.bottomright, 2)
            # button text
            text = font_btn.render(label, True, (255, 255, 255))
            self.screen.blit(text, (btn_rect.x + btn_rect.width//2 - text.get_width()//2,
                                    btn_rect.y + btn_rect.height//2 - text.get_height()//2))
        
        pygame.display.flip()
    
    def run(self):
        """Run the menu loop and return selected difficulty."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        return self.selected_difficulty if self.selected_difficulty else 'beginner'


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
        # header with 3D beveled effect
        pygame.draw.rect(self.screen, (192, 192, 192), (0, 0, self.width, HEADER_HEIGHT))
        # 3D top/left beveled edge (lighter)
        pygame.draw.line(self.screen, (255, 255, 255), (0, 0), (self.width, 0), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (0, 0), (0, HEADER_HEIGHT), 2)
        # 3D bottom/right beveled edge (darker)
        pygame.draw.line(self.screen, (128, 128, 128), (self.width-1, 0), (self.width-1, HEADER_HEIGHT), 2)
        pygame.draw.line(self.screen, (128, 128, 128), (0, HEADER_HEIGHT-1), (self.width, HEADER_HEIGHT-1), 2)

        font = pygame.font.SysFont(None, 24)
        remaining = max(0, self.board.mines - self.board.flagged_count)
        
        # Mines display with 3D inset effect
        mines_display_rect = pygame.Rect(8, 8, 70, 24)
        pygame.draw.rect(self.screen, (192, 192, 192), mines_display_rect)
        pygame.draw.line(self.screen, (128, 128, 128), mines_display_rect.topleft, mines_display_rect.topright, 1)
        pygame.draw.line(self.screen, (128, 128, 128), mines_display_rect.topleft, mines_display_rect.bottomleft, 1)
        pygame.draw.line(self.screen, (255, 255, 255), mines_display_rect.bottomleft, mines_display_rect.bottomright, 1)
        pygame.draw.line(self.screen, (255, 255, 255), mines_display_rect.topright, mines_display_rect.bottomright, 1)
        mines_txt = font.render(f"{remaining:03d}", True, (255, 0, 0))
        self.screen.blit(mines_txt, (mines_display_rect.x + 8, mines_display_rect.y + 4))

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

        timer_txt = font.render(f"{self.elapsed_seconds:03d}", True, (255, 0, 0))
        # Timer display with 3D inset effect
        timer_display_rect = pygame.Rect(self.width - 78, 8, 70, 24)
        pygame.draw.rect(self.screen, (192, 192, 192), timer_display_rect)
        pygame.draw.line(self.screen, (128, 128, 128), timer_display_rect.topleft, timer_display_rect.topright, 1)
        pygame.draw.line(self.screen, (128, 128, 128), timer_display_rect.topleft, timer_display_rect.bottomleft, 1)
        pygame.draw.line(self.screen, (255, 255, 255), timer_display_rect.bottomleft, timer_display_rect.bottomright, 1)
        pygame.draw.line(self.screen, (255, 255, 255), timer_display_rect.topright, timer_display_rect.bottomright, 1)
        self.screen.blit(timer_txt, (timer_display_rect.x + 8, timer_display_rect.y + 4))

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
    """Run the game with an optional difficulty.
    
    If difficulty is 'beginner' (default), show the difficulty menu first.
    Otherwise, start the game directly with the specified difficulty.
    """
    if difficulty == 'beginner':
        menu = DifficultyMenu()
        difficulty = menu.run()
    Game(difficulty).run()


if __name__ == '__main__':
    run()
