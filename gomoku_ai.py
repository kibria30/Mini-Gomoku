import numpy as np

class GomokuAI:
    def __init__(self, player_id=2, depth=2):
        self.player_id = player_id
        self.opponent_id = 3 - player_id
        self.depth = depth  # Keep depth small (2-3) for responsiveness
    
    def choose_move(self, game):
        if np.count_nonzero(game.board) == 0:
            return (game.board_size//2, game.board_size//2)
        
        valid_moves = self.get_reasonable_moves(game)
        if not valid_moves:
            return None
            
        best_score = -float('inf')
        best_move = valid_moves[0]
        
        for move in valid_moves:
            r, c = move
            game.board[r, c] = self.player_id
            score = self.minimax(game, self.depth-1, -float('inf'), float('inf'), False)
            game.board[r, c] = 0
            
            if score > best_score:
                best_score = score
                best_move = move
                # Early exit if we found a winning move
                if score == float('inf'):
                    break
        
        return best_move
    
    def minimax(self, game, depth, alpha, beta, is_maximizing):
        # Check for terminal states
        winner = self.check_winner(game)
        if winner == self.player_id:
            return float('inf')
        elif winner == self.opponent_id:
            return -float('inf')
        elif depth == 0 or len(game.get_valid_moves()) == 0:
            return self.fast_evaluate(game)
        
        valid_moves = self.get_reasonable_moves(game)
        
        if is_maximizing:
            value = -float('inf')
            for move in valid_moves:
                r, c = move
                game.board[r, c] = self.player_id
                value = max(value, self.minimax(game, depth-1, alpha, beta, False))
                game.board[r, c] = 0
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in valid_moves:
                r, c = move
                game.board[r, c] = self.opponent_id
                value = min(value, self.minimax(game, depth-1, alpha, beta, True))
                game.board[r, c] = 0
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
    
    def get_reasonable_moves(self, game):
        reasonable_moves = set()
        for r in range(game.board_size):
            for c in range(game.board_size):
                if game.board[r, c] != 0:
                    # Add all adjacent empty cells
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r+dr, c+dc
                            if (0 <= nr < game.board_size and 
                                0 <= nc < game.board_size and 
                                game.board[nr, nc] == 0):
                                reasonable_moves.add((nr, nc))
        
        # If no adjacent moves (unlikely), return all empty cells
        return list(reasonable_moves) if reasonable_moves else game.get_valid_moves()
    
    def fast_evaluate(self, game):
        score = 0
        
        # Check all possible 5-in-a-row segments
        for r in range(game.board_size):
            for c in range(game.board_size):
                # Horizontal
                if c <= game.board_size - 5:
                    segment = game.board[r, c:c+5]
                    score += self.score_segment(segment)
                # Vertical
                if r <= game.board_size - 5:
                    segment = game.board[r:r+5, c]
                    score += self.score_segment(segment)
                # Diagonal \
                if r <= game.board_size - 5 and c <= game.board_size - 5:
                    segment = [game.board[r+i, c+i] for i in range(5)]
                    score += self.score_segment(segment)
                # Diagonal /
                if r <= game.board_size - 5 and c >= 4:
                    segment = [game.board[r+i, c-i] for i in range(5)]
                    score += self.score_segment(segment)
        
        return score
    
    def score_segment(self, segment):
        ai_count = np.count_nonzero(segment == self.player_id)
        opp_count = np.count_nonzero(segment == self.opponent_id)
        
        if ai_count > 0 and opp_count > 0:
            return 0  # Blocked segment
        
        if ai_count == 0 and opp_count == 0:
            return 0  # Empty segment
        
        if opp_count > 0:
            return -10 ** opp_count  # Opponent threat
        else:
            return 10 ** ai_count  # AI opportunity
    
    def check_winner(self, game):
        for r in range(game.board_size):
            for c in range(game.board_size):
                if game.board[r, c] != 0 and game.check_win(r, c):
                    return game.board[r, c]
        return None