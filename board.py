from typing import List

class Board:

    SIZE = 8
    EMPTY = 0
    WHITE = 1
    BLACK = 2
    BACKGROUND_COLOR = (50, 168, 82)
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1)]

    def __init__(self) -> None:
        self.grid = self._reset_board()
        self.turn = Board.BLACK
    
    def _reset_board(self) -> List[List[int]]:
        new_grid = [[Board.EMPTY for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]
        new_grid[3][3] = Board.WHITE
        new_grid[4][4] = Board.WHITE
        new_grid[3][4] = Board.BLACK
        new_grid[4][3] = Board.BLACK

        return new_grid
    
    def handle_input(self, row, col):
        if (row, col) not in self._get_valid_moves():
            return
        self.grid = self._update_board(row, col)
        self.turn = self._opposite_turn(self.turn)
        # handle case in which there are no valid moves, skip turn
        if len(self._get_valid_moves()) == 0:
            self.turn = self._opposite_turn(self.turn)
    
    def _update_board(self, row, col) -> List[List[int]]:
        opposite_turn = self._opposite_turn(self.turn)
        new_grid = self.grid.copy()

        for next_dir in Board.DIRECTIONS:
            if self._is_sandwich(row, col, self.turn, next_dir):
                next_row = row + next_dir[0]
                next_col = col + next_dir[1]
                while self.grid[next_row][next_col] == opposite_turn:
                    new_grid[next_row][next_col] = self.turn
                    next_row = next_row + next_dir[0]
                    next_col = next_col + next_dir[1]

        new_grid[row][col] = self.turn
        return new_grid

    def _get_valid_moves(self) -> set[tuple]:
        valid_moves = set()
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if self._is_valid_move(i, j):
                    valid_moves.add((i, j))
        return valid_moves

    def _is_valid_move(self, row, col) -> bool:
        if self.grid[row][col] != Board.EMPTY:
            return False
        for next_dir in Board.DIRECTIONS:
            if self._is_sandwich(row, col, self.turn, next_dir):
                return True
        return False

    def _is_sandwich(self, row, col, turn, next_dir):
        new_row = row + next_dir[0] 
        new_col = col + next_dir[1] 
        opposite_turn = self._opposite_turn(turn)

        sandwich_count = 0
        while self._in_bounds(new_row, new_col):
            if self.grid[new_row][new_col] != opposite_turn:
                break

            sandwich_count += 1
            new_row = new_row + next_dir[0]
            new_col = new_col + next_dir[1]

        return self._in_bounds(new_row, new_col) and self.grid[new_row][new_col] == turn and sandwich_count > 0
    
    def _opposite_turn(self, turn):
        return Board.WHITE if turn == Board.BLACK else Board.BLACK
        
    def _in_bounds(self, row, col) -> bool:
        return row >= 0 and col >= 0 and row < Board.SIZE and col < Board.SIZE

    def game_ended(self) -> bool:
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if self.grid[i][j] == Board.EMPTY:
                    return False
        return True

    def render_board(self, pygame, screen, screen_size) -> None:
        screen.fill(Board.BACKGROUND_COLOR)
        line_width = 2
        black_color = (0, 0, 0)
        off_black_color = (50, 50, 50)
        white_color = (255, 255, 255)
        step_size = screen_size // Board.SIZE
        
        # draw lines
        for row in range(Board.SIZE + 1):
            row_coord = (row * step_size) - (line_width // 2)
            pygame.draw.line(screen, black_color, (row_coord, 0), (row_coord, screen_size), line_width) 

        for col in range(Board.SIZE):
            col_coord = (col * step_size) - (line_width // 2)
            pygame.draw.line(screen, black_color, (0, col_coord), (screen_size, col_coord), line_width) 

        circle_radius = (step_size // 2) - (line_width * 2)

        # draw pieces
        for row in range(Board.SIZE):
            row_coord = (row * step_size) + circle_radius + (line_width * 2)
            for col in range(Board.SIZE):
                col_coord = (col * step_size) + circle_radius + (line_width * 2)
                elem = self.grid[row][col]
                if elem == Board.WHITE:
                    pygame.draw.circle(screen, white_color, (col_coord, row_coord), circle_radius)
                    pygame.draw.circle(screen, black_color, (col_coord, row_coord), circle_radius, line_width)
                elif elem == Board.BLACK:
                    pygame.draw.circle(screen, off_black_color, (col_coord, row_coord), circle_radius)
                    pygame.draw.circle(screen, black_color, (col_coord, row_coord), circle_radius, line_width)
                elif self._is_valid_move(row, col):
                    pygame.draw.circle(screen, off_black_color, (col_coord, row_coord), circle_radius, line_width)
    
    def get_count(self, color):
        if color != Board.BLACK and color != Board.WHITE:
            raise ValueError("color " + color + " not Board.BLACK or Board.WHITE")
        count = 0
        
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                if self.grid[row][col] == color:
                    count += 1
        
        return count
    
    def print_board(self):
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                print(self.grid[row][col], end=" ")
            print()
        print()