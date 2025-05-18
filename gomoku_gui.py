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
    
    def setup_ui(self):
        """Setup the enhanced user interface"""
        self.root.title("Gomoku Pro")
        self.root.geometry("600x700")
        self.root.minsize(550, 650)
        
        # Main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Board frame
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.TOP, pady=(0, 10))
        
        # Create canvas with better styling
        self.canvas_size = self.board_size * self.cell_size
        self.canvas = tk.Canvas(
            self.board_frame, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg="#DCB35C",  # Wooden board color
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Control panel with better layout
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=5)
        
        # Status label with improved styling
        self.status_var = tk.StringVar()
        self.status_var.set("Your turn (Black)")
        self.status_label = tk.Label(
            self.control_frame,
            textvariable=self.status_var,
            font=("Helvetica", 12, "bold"),
            fg="#333333"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, expand=True, anchor="w")
        
        # Stats button
        self.stats_btn = tk.Button(
            self.control_frame,
            text="Stats",
            command=self.show_stats,
            font=("Helvetica", 10),
            bg="#f0f0f0"
        )
        self.stats_btn.pack(side=tk.LEFT, padx=5)
        
        # Hint button
        self.hint_btn = tk.Button(
            self.control_frame,
            text="Hint",
            command=self.show_hint,
            font=("Helvetica", 10),
            bg="#f0f0f0"
        )
        self.hint_btn.pack(side=tk.LEFT, padx=5)
        
        # Settings button
        self.settings_btn = tk.Button(
            self.control_frame,
            text="AI Settings",
            command=self.show_settings,
            font=("Helvetica", 10),
            bg="#f0f0f0"
        )
        self.settings_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button with better styling
        self.reset_btn = tk.Button(
            self.control_frame,
            text="New Game",
            command=self.reset_game,
            font=("Helvetica", 10),
            bg="#4CAF50",
            fg="white"
        )
        self.reset_btn.pack(side=tk.RIGHT, padx=5)
        
        # Move history panel
        self.history_frame = tk.Frame(self.main_frame)
        self.history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_label = tk.Label(
            self.history_frame,
            text="Move History:",
            font=("Helvetica", 10),
            anchor="w"
        )
        self.history_label.pack(fill=tk.X)
        
        self.history_text = tk.Text(
            self.history_frame,
            height=6,
            font=("Courier", 9),
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Draw the initial board
        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.waiting_for_ai = False
        self.ai_thread = None
     
    def draw_board(self):
        """Draw the enhanced Gomoku board"""
        self.canvas.delete("all")
        
        # Draw grid with better styling
        for i in range(self.board_size):
            # Horizontal lines
            self.canvas.create_line(
                0, i * self.cell_size + self.cell_size // 2,
                self.canvas_size, i * self.cell_size + self.cell_size // 2,
                width=1.5, fill="#8B4513"  # SaddleBrown
            )
            # Vertical lines
            self.canvas.create_line(
                i * self.cell_size + self.cell_size // 2, 0,
                i * self.cell_size + self.cell_size // 2, self.canvas_size,
                width=1.5, fill="#8B4513"
            )
        
        # Draw star points with better visibility
        star_points = self.get_star_points()
        for point in star_points:
            r, c = point
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5,
                fill="#8B0000", outline="#8B0000"  # DarkRed
            )
        
        # Highlight last move if exists
        if self.game.last_move:
            self.highlight_last_move(*self.game.last_move)
        
        # Draw stones
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.game.board[r, c] != 0:
                    self.draw_stone(r, c)
    
    def get_star_points(self):
        """Get positions for star points based on board size"""
        if self.board_size >= 15:
            return [(3, 3), (3, 11), (3, self.board_size-4),
                    (7, 7),
                    (self.board_size-4, 3), (self.board_size-4, 11), (self.board_size-4, self.board_size-4)]
        else:
            mid = self.board_size // 2
            offset = min(2, mid - 1)
            return [
                (mid - offset, mid - offset), 
                (mid - offset, mid + offset), 
                (mid + offset, mid - offset), 
                (mid + offset, mid + offset)
            ]
    
    def draw_stone(self, row, col):
        """Draw a stone with enhanced appearance"""
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        radius = int(self.cell_size * 0.42)
        
        if self.game.board[row, col] == 1:  # Player (black)
            # Create a glossy black stone
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill="black", outline="#333333", width=1
            )
            self.canvas.create_oval(
                x - radius//2, y - radius//2, x + radius//3, y + radius//3,
                fill="#555555", outline=""
            )
        else:  # AI (white)
            # Create a glossy white stone
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill="white", outline="#CCCCCC", width=1
            )
            self.canvas.create_oval(
                x - radius//2, y - radius//2, x + radius//3, y + radius//3,
                fill="#F8F8F8", outline=""
            )
    
    def handle_click(self, event):
        pass
        # soon
    
    def ai_move(self):
        pass
        # soon

    def show_game_result(self):
        pass
        #soon to 

    def reset_game(self):
        pass
        # I will do this near future.


def run_gui():
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()