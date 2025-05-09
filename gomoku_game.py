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
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1
        self.last_move = None
        self.game_over = False
        self.winner = None
    
    def is_valid_move(self, row, col):
        """Check if a move is valid (in bounds and cell is empty)."""
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row, col] == 0
        return False
    
    def make_move(self, row, col):
        if not self.is_valid_move(row, col) or self.game_over:
            return False
        
        self.board[row, col] = self.current_player
        self.last_move = (row, col)
        
        # Check if this move results in a win
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
        # Check if the board is full (draw)
        elif np.count_nonzero(self.board) == self.board_size * self.board_size:
            self.game_over = True
            self.winner = 0  # Draw
        else:
            # Switch to the other player
            self.current_player = 3 - self.current_player  # Alternates between 1 and 2
        
        return True