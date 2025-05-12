from gomoku_game import GomokuGame
from gomoku_ai import GomokuAI
import time

class ConsoleGame:
    def __init__(self, board_size=10):
        self.game = GomokuGame(board_size)
        self.ai = GomokuAI(max_depth=3, time_limit=2)
        self.ai_enabled = False
    
    def print_board(self):
        print(self.game)
    
    def get_player_move(self):
        while True:
            try:
                move = input(f"Player {self.game.current_player}, enter your move (row col): ")
                row, col = map(int, move.split())
                if self.game.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter two numbers separated by a space.")
    
    def get_ai_move(self):
        print("AI is thinking...")
        start_time = time.time()
        row, col = self.ai.choose_move(self.game)
        elapsed = time.time() - start_time
        print(f"AI chose ({row}, {col}) in {elapsed:.2f} seconds")
        return row, col
    
    def play_turn(self):
        self.print_board()
        
        if self.game.current_player == 1 or not self.ai_enabled:
            # Human player's turn
            row, col = self.get_player_move()
        else:
            # AI's turn
            row, col = self.get_ai_move()
        
        self.game.make_move(row, col)
    
    def play(self):
        print("Welcome to Gomoku!")
        print("Choose game mode:")
        print("1. Two players")
        print("2. Player vs AI")
        
        while True:
            choice = input("Enter 1 or 2: ")
            if choice == '1':
                self.ai_enabled = False
                break
            elif choice == '2':
                self.ai_enabled = True
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        
        print("Players take turns entering moves as 'row col' (0-based indices).")
        
        while not self.game.game_over:
            self.play_turn()
        
        self.print_board()
        if self.game.winner == 0:
            print("Game over! It's a draw!")
        else:
            winner = "AI" if (self.game.winner == 2 and self.ai_enabled) else f"Player {self.game.winner}"
            print(f"Game over! {winner} wins!")
        
        play_again = input("Play again? (y/n): ").lower()
        if play_again == 'y':
            self.game.reset_game()
            self.play()

def main():
    """Main function to start the console game."""
    game = ConsoleGame()
    game.play()

if __name__ == "__main__":
    main()