import tkinter as tk
from tkinter import messagebox
import time
from gomoku_game import GomokuGame
from gomoku_ai import GomokuAI

class GomokuGUI:

    def __init__(self, root, board_size=10, cell_size=50):
        self.root = root
        self.board_size = board_size
        self.cell_size = cell_size
        
        self.game = GomokuGame(board_size)
        self.ai = GomokuAI(max_depth=3, time_limit=2)
        
        self.root.title("Gomoku Game")
        self.canvas_size = board_size * cell_size
        
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(padx=10, pady=10)
        
        self.canvas = tk.Canvas(
            self.board_frame, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg="#E8B96F"  # Light wood color
        )
        self.canvas.pack()
        
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Your turn (Black)")
        self.status_label = tk.Label(
            self.control_frame, 
            textvariable=self.status_var,
            font=("Arial", 12)
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(
            self.control_frame, 
            text="New Game", 
            command=self.reset_game,
            font=("Arial", 10)
        )
        self.reset_button.pack(side=tk.RIGHT, padx=10)
        
        self.draw_board()
        
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.waiting_for_ai = False
    

    def draw_board(self):
        # under construction



    def draw_stone(self, row, col):
        # def under construction

    def handle_click(self, event):
        # soon
    
    def ai_move(self):
        # soon

    def show_game_result(self):
        #soon to 

    def reset_game(self):
        # I will do this near future.


def run_gui():
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()