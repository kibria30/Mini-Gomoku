import numpy as np
import time

class GomokuAI:

    
    def __init__(self, max_depth=3, time_limit=2, player_id=2):

        self.max_depth = max_depth
        self.time_limit = time_limit
        self.player_id = player_id  # AI player (usually 2)
        self.opponent_id = 3 - player_id  # Human player (usually 1)
        self.start_time = 0
        self.nodes_evaluated = 0
        self.transposition_table = {}  # For storing evaluated positions