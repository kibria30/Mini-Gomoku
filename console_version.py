from gomoku_game import GomokuGame
from gomoku_ai import GomokuAI

class ConsoleGame:
    def __init__(self, board_size=10):
        self.game = GomokuGame(board_size)
        self.ai = GomokuAI()
    
    def print_board(self):
        print(self.game)
    
    def get_player_move(self):
        while True:
            try:
                move = input(f"Player {self.game.current_player}, enter move (row col): ")
                row, col = map(int, move.split())
                if self.game.is_valid_move(row, col):
                    return (row, col)
                print("Invalid move! Try again.")
            except:
                print("Enter two numbers separated by space!")
    
    def play(self):
        print("Welcome to Gomoku!")
        print("Player 1: X, Player 2: O")
        
        while not self.game.game_over:
            self.print_board()
            
            if self.game.current_player == 1:
                row, col = self.get_player_move()
            else:
                print("AI is thinking...")
                row, col = self.ai.choose_move(self.game)
            
            self.game.make_move(row, col)
        
        self.print_board()
        if self.game.winner == 0:
            print("It's a draw!")
        else:
            print(f"Player {self.game.winner} wins!")

def main():
    game = ConsoleGame()
    game.play()

if __name__ == "__main__":
    main()