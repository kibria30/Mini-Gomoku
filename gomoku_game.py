import numpy as np

class GomokuGame:
    def __init__(self, board_size=10):
        """Initialize an empty Gomoku board."""
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = 1  # Player 1 (human) starts
        self.last_move = None
        self.game_over = False
        self.winner = None
        self.move_history = []

    def reset_game(self):
        """Reset the game to initial state."""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1
        self.last_move = None
        self.game_over = False
        self.winner = None
        self.move_history.clear()

    def is_valid_move(self, row, col):
        """Check if a move is valid (in bounds and cell is empty)."""
        return 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row, col] == 0

    def make_move(self, row, col):
        if not self.is_valid_move(row, col) or self.game_over:
            return False

        self.board[row, col] = self.current_player
        self.last_move = (row, col)
        self.move_history.append((row, col, self.current_player))

        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
        elif np.count_nonzero(self.board) == self.board_size * self.board_size:
            self.game_over = True
            self.winner = 0  # Draw
        else:
            self.current_player = 3 - self.current_player

        return True

    def undo_move(self):
        """Undo the last move made on the board."""
        if not self.move_history:
            return False

        row, col, player = self.move_history.pop()
        self.board[row, col] = 0
        self.current_player = player
        self.game_over = False
        self.winner = None

        if self.move_history:
            self.last_move = (self.move_history[-1][0], self.move_history[-1][1])
        else:
            self.last_move = None

        return True

    def check_win(self, row, col):
        """Check if the last move at (row, col) resulted in 5 in a row."""
        player = self.board[row, col]
        directions = [
            [(0, 1), (0, -1)],
            [(1, 0), (-1, 0)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]

        for dir_pair in directions:
            count = 1
            for dr, dc in dir_pair:
                r, c = row, col
                for _ in range(4):
                    r, c = r + dr, c + dc
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == player:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True

        return False

    def get_valid_moves(self):
        """Return a list of all valid moves on the board."""
        return [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r, c] == 0]

    def get_board_copy(self):
        """Return a deep copy of the current board state."""
        return self.board.copy()

    def get_board_state(self):
        """Return a tuple of (board, current_player, game_over, winner)."""
        return (self.board.copy(), self.current_player, self.game_over, self.winner)

    def __str__(self):
        """String representation of the board."""
        symbols = {0: ".", 1: "X", 2: "O"}
        result = "  " + " ".join(str(i) for i in range(self.board_size)) + "\n"
        for i in range(self.board_size):
            result += f"{i} " + " ".join(symbols[self.board[i, j]] for j in range(self.board_size)) + "\n"
        return result

    def is_empty_board(self):
        """Return True if the board has no moves."""
        return np.count_nonzero(self.board) == 0
