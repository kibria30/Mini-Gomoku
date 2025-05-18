"""
Enhanced Gomoku Game GUI

This module implements a professional and visually appealing graphical user interface 
for the Gomoku game using Tkinter with advanced styling and features.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import time
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
from gomoku_game import GomokuGame
from gomoku_ai import GomokuAI

class ModernButton(tk.Canvas):
    """Custom button with modern styling and hover effects"""
    
    def __init__(self, parent, text, command, width=120, height=40, bg="#4a6fa5", hover_bg="#345785", 
                 fg="white", corner_radius=10, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"],
                         highlightthickness=0, **kwargs)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.fg = fg
        self.corner_radius = corner_radius
        self.text = text
        
        # Initial state
        self.state = 'normal'
        
        # Create the button
        self.create_rounded_button()
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def create_rounded_button(self):
        """Create the rounded rectangle button with text"""
        self.delete("all")
        
        bg_color = self.bg if self.state != 'hover' else self.hover_bg
        
        # Draw rounded rectangle
        self.create_rounded_rect(0, 0, self.winfo_width(), self.winfo_height(), 
                                self.corner_radius, fill=bg_color, outline="")
        
        # Add text
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, 
                         text=self.text, fill=self.fg, 
                         font=("Arial", 11, "bold"))
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def on_enter(self, event):
        """Mouse enter effect"""
        self.state = 'hover'
        self.create_rounded_button()
    
    def on_leave(self, event):
        """Mouse leave effect"""
        self.state = 'normal'
        self.create_rounded_button()
    
    def on_press(self, event):
        """Mouse press effect"""
        self.state = 'pressed'
        self.create_rounded_button()
    
    def on_release(self, event):
        """Execute command on button release"""
        if self.state == 'pressed':
            self.command()
        self.state = 'normal'
        self.create_rounded_button()
        
    def configure(self, **kwargs):
        """Configure button properties"""
        if 'text' in kwargs:
            self.text = kwargs.pop('text')
        if 'bg' in kwargs:
            self.bg = kwargs.pop('bg')
        if 'hover_bg' in kwargs:
            self.hover_bg = kwargs.pop('hover_bg')
        if 'fg' in kwargs:
            self.fg = kwargs.pop('fg')
            
        super().configure(**kwargs)
        self.create_rounded_button()


class GomokuGUI:
    """
    Enhanced GUI for the Gomoku game using Tkinter with modern styling.
    """
    
    def __init__(self, root, board_size=15, cell_size=40):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
            board_size: Size of the Gomoku board (default is 15)
            cell_size: Size of each cell in pixels (default is 40)
        """
        self.root = root
        self.board_size = board_size
        self.cell_size = cell_size
        
        # Setup theme colors
        self.colors = {
            "bg_main": "#f0f0f0",           # Light gray background
            "bg_board": "#E8B96F",           # Board background (light wood)
            "board_dark": "#D19C45",         # Darker wood for grid lines
            "text_dark": "#333333",          # Dark text
            "text_light": "#FFFFFF",         # Light text
            "player_stone": "#000000",       # Black stone
            "ai_stone": "#FFFFFF",           # White stone
            "highlight": "#FF4500",          # Highlight color (orange-red)
            "btn_primary": "#4a6fa5",        # Blue buttons
            "btn_danger": "#d9534f",         # Red buttons
            "btn_hover": "#345785",          # Button hover state
            "status_player": "#2c3e50",      # Player turn status
            "status_ai": "#c0392b"           # AI turn status
        }
        
        # Default font styles
        self.fonts = {
            "title": font.Font(family="Arial", size=16, weight="bold"),
            "status": font.Font(family="Arial", size=12),
            "normal": font.Font(family="Arial", size=10),
            "button": font.Font(family="Arial", size=10, weight="bold")
        }
        
        # Set up the game logic
        self.game = GomokuGame(board_size)
        
        # Game settings
        self.difficulty = tk.StringVar(value="Normal")
        self.ai_player = GomokuAI(max_depth=3, time_limit=2)  # Default: Normal
        self.pass_and_play = tk.BooleanVar(value=False)
        self.show_last_move = tk.BooleanVar(value=True)
        self.last_move = None
        self.stone_images = {}  # Cache for stone images
        
        # Set up window properties
        self.root.title("Gomoku - Five in a Row")
        self.root.geometry(f"{900}x{650}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors["bg_main"])
        
        # Try to set icon if available
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass  # Ignore if icon is not available
        
        # Create main container
        self.main_frame = tk.Frame(root, bg=self.colors["bg_main"])
        self.main_frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
        
        # Create title frame
        self.create_title_frame()
        
        # Create content frame that holds board and sidebar
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create board frame (left side)
        self.create_board_frame()
        
        # Create sidebar frame (right side)
        self.create_sidebar_frame()
        
        # Create status bar
        self.create_status_bar()
        
        # Initialize the game
        self.draw_board()
        
        # Flag to prevent clicks during AI's turn
        self.waiting_for_ai = False
        
    def create_title_frame(self):
        """Create the title section"""
        title_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"], height=50)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame, 
            text="GOMOKU", 
            font=("Arial", 22, "bold"),
            fg=self.colors["text_dark"],
            bg=self.colors["bg_main"]
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            title_frame, 
            text="FIVE IN A ROW", 
            font=("Arial", 12),
            fg=self.colors["text_dark"],
            bg=self.colors["bg_main"]
        )
        subtitle_label.pack(side=tk.LEFT, padx=15, pady=8)
    
    def create_board_frame(self):
        """Create the frame containing the game board"""
        # Container for the board with border effect
        self.board_container = tk.Frame(
            self.content_frame,
            bg="#7D5A2A",  # Darker wood frame
            padx=3,
            pady=3,
            bd=0,
            highlightthickness=0
        )
        self.board_container.pack(side=tk.LEFT, padx=(0, 15))
        
        # Canvas size includes margins
        self.canvas_size = self.board_size * self.cell_size
        
        # Create the canvas for drawing the board
        self.canvas = tk.Canvas(
            self.board_container, 
            width=self.canvas_size, 
            height=self.canvas_size, 
            bg=self.colors["bg_board"],
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack()
        
        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.handle_click)
    
    def create_sidebar_frame(self):
        """Create the sidebar with game controls"""
        self.side_frame = tk.Frame(self.content_frame, bg=self.colors["bg_main"], width=200)
        self.side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        self.side_frame.pack_propagate(False)  # Prevent shrinking
        
        # Game Info Section
        info_frame = tk.LabelFrame(
            self.side_frame, 
            text="Game Info", 
            bg=self.colors["bg_main"], 
            fg=self.colors["text_dark"],
            font=self.fonts["normal"]
        )
        info_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Player info
        tk.Label(
            info_frame, 
            text="You: Black (●)", 
            font=self.fonts["normal"], 
            bg=self.colors["bg_main"], 
            fg=self.colors["text_dark"],
            anchor="w"
        ).pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(
            info_frame, 
            text="Opponent: White (○)", 
            font=self.fonts["normal"], 
            bg=self.colors["bg_main"], 
            fg=self.colors["text_dark"],
            anchor="w"
        ).pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Game Settings Section
        settings_frame = tk.LabelFrame(
            self.side_frame, 
            text="Game Settings", 
            bg=self.colors["bg_main"], 
            fg=self.colors["text_dark"],
            font=self.fonts["normal"]
        )
        settings_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Difficulty selection
        diff_frame = tk.Frame(settings_frame, bg=self.colors["bg_main"])
        diff_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(
            diff_frame, 
            text="Difficulty:", 
            font=self.fonts["normal"], 
            bg=self.colors["bg_main"],
            fg=self.colors["text_dark"],
            width=10,
            anchor="w"
        ).pack(side=tk.LEFT)
        
        diff_options = ["Easy", "Normal", "Hard", "Expert"]
        diff_dropdown = ttk.Combobox(
            diff_frame, 
            textvariable=self.difficulty,
            values=diff_options,
            width=8,
            state="readonly"
        )
        diff_dropdown.pack(side=tk.RIGHT, padx=(0, 5))
        diff_dropdown.bind("<<ComboboxSelected>>", self.change_difficulty)
        
        # Pass and Play option
        pnp_frame = tk.Frame(settings_frame, bg=self.colors["bg_main"])
        pnp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Checkbutton(
            pnp_frame,
            text="Pass and Play",
            variable=self.pass_and_play,
            bg=self.colors["bg_main"],
            fg=self.colors["text_dark"],
            selectcolor=self.colors["bg_main"],
            font=self.fonts["normal"],
            command=self.toggle_pass_and_play
        ).pack(side=tk.LEFT)
        
        # Show last move option
        last_move_frame = tk.Frame(settings_frame, bg=self.colors["bg_main"])
        last_move_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Checkbutton(
            last_move_frame,
            text="Highlight Last Move",
            variable=self.show_last_move,
            bg=self.colors["bg_main"],
            fg=self.colors["text_dark"],
            selectcolor=self.colors["bg_main"],
            font=self.fonts["normal"],
            command=self.draw_board
        ).pack(side=tk.LEFT)
        
        # Actions Section
        actions_frame = tk.LabelFrame(
            self.side_frame, 
            text="Actions", 
            bg=self.colors["bg_main"], 
            fg=self.colors["text_dark"],
            font=self.fonts["normal"]
        )
        actions_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Button frame for centering
        button_frame = tk.Frame(actions_frame, bg=self.colors["bg_main"])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # New Game button
        new_game_btn = ModernButton(
            button_frame,
            text="New Game",
            command=self.reset_game,
            bg=self.colors["btn_primary"],
            hover_bg=self.colors["btn_hover"],
            fg=self.colors["text_light"],
            width=160,
            height=35
        )
        new_game_btn.pack(pady=(0, 10))
        
        # Undo button
        undo_btn = ModernButton(
            button_frame,
            text="Undo Move",
            command=self.undo_move,
            bg=self.colors["btn_primary"],
            hover_bg=self.colors["btn_hover"],
            fg=self.colors["text_light"],
            width=160,
            height=35
        )
        undo_btn.pack(pady=(0, 10))
    
        # Help button
        help_btn = ModernButton(
            button_frame,
            text="Help",
            command=self.show_help,
            bg=self.colors["btn_primary"],
            hover_bg=self.colors["btn_hover"],
            fg=self.colors["text_light"],
            width=160,
            height=35
        )
        help_btn.pack()
        
        # Credits
        credit_frame = tk.Frame(self.side_frame, bg=self.colors["bg_main"])
        credit_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        tk.Label(
            credit_frame,
            text="© 2025 Gomoku Pro",
            font=("Arial", 8),
            fg=self.colors["text_dark"],
            bg=self.colors["bg_main"]
        ).pack()
    
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"], height=40)
        self.status_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Your turn (Black)")
        self.status_label = tk.Label(
            self.status_frame, 
            textvariable=self.status_var,
            font=self.fonts["status"],
            bg=self.colors["status_player"],
            fg=self.colors["text_light"],
            padx=10,
            pady=5
        )
        self.status_label.pack(fill=tk.X)
    
    def toggle_pass_and_play(self):
        """Toggle between AI opponent and pass-and-play mode"""
        self.reset_game()
        if self.pass_and_play.get():
            self.status_var.set("Black's turn")
        else:
            self.status_var.set("Your turn (Black)")
    
    def change_difficulty(self, event=None):
        """Update AI difficulty settings"""
        difficulty = self.difficulty.get()
        
        # Configure AI based on difficulty
        if difficulty == "Easy":
            self.ai_player = GomokuAI(max_depth=1, time_limit=1)
        elif difficulty == "Normal":
            self.ai_player = GomokuAI(max_depth=2, time_limit=2)
        elif difficulty == "Hard":
            self.ai_player = GomokuAI(max_depth=3, time_limit=3)
        elif difficulty == "Expert":
            self.ai_player = GomokuAI(max_depth=5, time_limit=7)
        
        # Reset the game if it's in progress
        if not self.game.is_empty_board():
            if messagebox.askyesno("Change Difficulty", 
                                   "Changing difficulty will start a new game. Continue?"):
                self.reset_game()
            else:
                # Revert to previous selection
                old_difficulties = {"Easy": 1, "Normal": 2, "Hard": 3, "Expert": 5}
                for diff, depth in old_difficulties.items():
                    if self.ai_player.max_depth == depth:
                        self.difficulty.set(diff)
                        break
    
    def draw_board(self):
        """Draw the Gomoku board with grid lines and points."""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Draw the wooden background texture
        self.create_board_texture()
        
        # Draw grid lines
        for i in range(self.board_size):
            # Horizontal lines
            self.canvas.create_line(
                self.cell_size // 2, i * self.cell_size + self.cell_size // 2,
                self.canvas_size - self.cell_size // 2, i * self.cell_size + self.cell_size // 2,
                width=1.5,
                fill=self.colors["board_dark"]
            )
            # Vertical lines
            self.canvas.create_line(
                i * self.cell_size + self.cell_size // 2, self.cell_size // 2,
                i * self.cell_size + self.cell_size // 2, self.canvas_size - self.cell_size // 2,
                width=1.5,
                fill=self.colors["board_dark"]
            )
        
        # Draw star points (traditional Gomoku board has star points)
        star_points = []
        if self.board_size >= 15:  # Traditional star points for 15x15 board
            star_points = [(3, 3), (3, 7), (3, 11), (7, 3), (7, 7), (7, 11), (11, 3), (11, 7), (11, 11)]
        elif self.board_size >= 13:  # For 13x13 board
            star_points = [(3, 3), (3, 9), (6, 6), (9, 3), (9, 9)]
        else:  # For smaller boards
            mid = self.board_size // 2
            offset = 2
            star_points = [
                (mid - offset, mid - offset), 
                (mid - offset, mid + offset), 
                (mid, mid),
                (mid + offset, mid - offset), 
                (mid + offset, mid + offset)
            ]
        
        for point in star_points:
            r, c = point
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(
                x - 4, y - 4, x + 4, y + 4,
                fill=self.colors["board_dark"],
                outline=""
            )
        
        # Draw stones and highlight last move if needed
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.game.board[r, c] != 0:
                    self.draw_stone(r, c)
    
    def create_board_texture(self):
        """Create a subtle wood texture for the board"""
        self.canvas.create_rectangle(
            0, 0, self.canvas_size, self.canvas_size,
            fill=self.colors["bg_board"], outline=""
        )
    
    def create_stone_image(self, color, size):
        """Create a stone image with realistic 3D effect"""
        # Create a unique key for the cache
        cache_key = f"{color}_{size}"
        
        # Check if we already created this image
        if cache_key in self.stone_images:
            return self.stone_images[cache_key]
        
        # Image size with padding for shadow
        img_size = int(size * 1.2)
        center = img_size // 2
        
        # Create a new transparent image
        image = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        radius = size // 2 - 2
        
        if color == "black":
            # Black stone with highlight
            draw.ellipse((center-radius, center-radius, center+radius, center+radius), 
                         fill=(30, 30, 30, 255))
            # Add highlight
            highlight_radius = radius * 0.7
            highlight_offset = radius * 0.25
            draw.ellipse((center-highlight_radius+highlight_offset, 
                          center-highlight_radius-highlight_offset, 
                          center+highlight_radius-highlight_offset, 
                          center-highlight_radius*0.3-highlight_offset), 
                         fill=(80, 80, 80, 120))
        else:
            # White stone with shadow and highlight
            draw.ellipse((center-radius, center-radius, center+radius, center+radius), 
                         fill=(240, 240, 240, 255))
            # Add shadow on bottom right
            draw.ellipse((center-radius+2, center-radius+2, center+radius, center+radius), 
                         fill=(200, 200, 200, 200))
            # Add highlight on top left
            highlight_radius = radius * 0.6
            highlight_offset = radius * 0.3
            draw.ellipse((center-highlight_radius-highlight_offset, 
                          center-highlight_radius-highlight_offset, 
                          center+highlight_radius-highlight_offset, 
                          center-highlight_radius*0.4-highlight_offset), 
                         fill=(255, 255, 255, 180))
        
        # Apply slight blur for smoother edges
        image = image.filter(ImageFilter.GaussianBlur(1))
        
        # Convert to PhotoImage
        photo_image = ImageTk.PhotoImage(image)
        
        # Store in cache
        self.stone_images[cache_key] = photo_image
        
        return photo_image
    
    def draw_stone(self, row, col):
        """Draw a stone at the specified position with 3D effect."""
        if self.game.board[row, col] != 0:
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            stone_size = int(self.cell_size * 0.8)  # Size of the stone
            
            # Determine stone color
            if self.game.board[row, col] == 1:  # Player (black)
                stone_image = self.create_stone_image("black", stone_size)
            else:  # AI or second player (white)
                stone_image = self.create_stone_image("white", stone_size)
            
            # Create the stone image
            self.canvas.create_image(x, y, image=stone_image, tags=f"stone_{row}_{col}")
            
            # Highlight last move if needed
            if self.show_last_move.get() and self.last_move == (row, col):
                marker_size = int(self.cell_size * 0.2)
                self.canvas.create_oval(
                    x - marker_size, y - marker_size,
                    x + marker_size, y + marker_size,
                    outline=self.colors["highlight"],
                    width=2
                )
    
    def handle_click(self, event):
        """Handle mouse click events on the board."""
        if self.waiting_for_ai or self.game.game_over:
            return
        
        # Convert pixel coordinates to board indices
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Make sure we're within bounds
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            # Try to make the move
            if self.game.make_move(row, col):
                # Update the display and last move highlight
                self.last_move = (row, col)
                self.draw_board()
                
                # Check if the game is over
                if self.game.check_win(row, col):
                    self.game.game_over = True
                    self.game.winner = self.game.current_player
                    self.show_game_result()
                    return
                
                if self.pass_and_play.get():
                    # Pass and play mode - switch player
                    player_name = "White" if self.game.current_player == 2 else "Black"
                    self.status_var.set(f"{player_name}'s turn")
                    self.status_label.configure(
                        bg=self.colors["status_ai"] if player_name == "White" else self.colors["status_player"]
                    )
                else:
                    # AI mode - computer's turn
                    self.waiting_for_ai = True
                    self.status_var.set("AI is thinking...")
                    self.status_label.configure(bg=self.colors["status_ai"])
                    self.root.update()  # Update the display
                    
                    # Use a slight delay before the AI's move
                    self.root.after(200, self.ai_move)
    
    def ai_move(self):
        """Make a move for the AI."""
        # Get the AI's move
        start_time = time.time()
        row, col = self.ai_player.choose_move(self.game)
        elapsed = time.time() - start_time
        
        if row is not None and col is not None:
            # Make the move
            self.game.make_move(row, col)
            
            # Update the last move highlight
            self.last_move = (row, col)
            
            # Update the display
            self.draw_board()
            
            # Check if the game is over
            if self.game.check_win(row, col):
                self.game.game_over = True
                self.game.winner = self.game.current_player
                self.show_game_result()
            else:
                self.status_var.set(f"Your turn (Black) - AI took {elapsed:.1f}s")
                self.status_label.configure(bg=self.colors["status_player"])
        
        self.waiting_for_ai = False
    
    def show_game_result(self):
        """Show the game result with improved styling."""
        if self.pass_and_play.get():
            winner_text = "Black" if self.game.winner == 1 else "White"
            self.status_var.set(f"{winner_text} wins!")
            messagebox.showinfo("Game Over", f"{winner_text} wins!")
        else:
            if self.game.winner == 1:  # Player wins
                self.status_var.set("You won!")
                self.status_label.configure(bg=self.colors["status_player"])
                messagebox.showinfo("Game Over", "Congratulations! You won!")
            elif self.game.winner == 2:  # AI wins
                self.status_var.set("AI won!")
                self.status_label.configure(bg=self.colors["status_ai"])
                messagebox.showinfo("Game Over", "AI won this round!")
            else:  # Draw
                self.status_var.set("It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.game.reset_game()
        self.last_move = None
        self.draw_board()
        self.waiting_for_ai = False
        
        if self.pass_and_play.get():
            self.status_var.set("Black's turn")
        else:
            self.status_var.set("Your turn (Black)")
            
        self.status_label.configure(bg=self.colors["status_player"])
    
    def undo_move(self):
        """Undo the last move(s)"""
        if self.game.game_over:
            return
        
        if self.pass_and_play.get():
            # Undo just one move in pass and play
            if self.game.undo_move():
                self.last_move = None
                self.draw_board()
                player_name = "Black" if self.game.current_player == 1 else "White"
                self.status_var.set(f"{player_name}'s turn")
                self.status_label.configure(
                    bg=self.colors["status_player"] if player_name == "Black" else self.colors["status_ai"]
                )
        else:
            # In AI mode, undo both player's and AI's last moves
            # Undo twice to get back to player's turn
            if self.game.undo_move() and self.game.undo_move():
                self.last_move = None
                self.draw_board()
                self.status_var.set("Your turn (Black)")
                self.status_label.configure(bg=self.colors["status_player"])
            else:
                messagebox.showinfo("Undo", "Nothing to undo!")
    
    def show_help(self):
        """Show game rules and instructions"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Gomoku Help")
        help_window.geometry("500x400")
        help_window.configure(bg=self.colors["bg_main"])
        help_window.resizable(False, False)
        
        # Make it modal
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Title
        tk.Label(
            help_window, 
            text="How to Play Gomoku",
            font=("Arial", 16, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_dark"]
        ).pack(pady=(20, 5))
        
        # Rules frame
        rules_frame = tk.Frame(help_window, bg=self.colors["bg_main"], padx=30, pady=10)
        rules_frame.pack(fill=tk.BOTH, expand=True)
        
        # Game rules
        rules = [
            "• Gomoku (also called Five in a Row) is played on a square grid.",
            "• Players take turns placing their stones on empty intersections.",
            "• Black always plays first.",
            "• The goal is to form an unbroken chain of 5 stones horizontally,",
            "  vertically, or diagonally.",
            "• The first player to create such a chain wins.",
            "• There is no capturing in the standard version of Gomoku."
        ]
        
        for rule in rules:
            tk.Label(
                rules_frame,
                text=rule,
                font=("Arial", 11),
                bg=self.colors["bg_main"],
                fg=self.colors["text_dark"],
                anchor="w",
                justify=tk.LEFT
            ).pack(fill=tk.X, pady=3)
        
        # Game modes section
        tk.Label(
            rules_frame, 
            text="Game Modes:",
            font=("Arial", 11, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_dark"],
            anchor="w"
        ).pack(fill=tk.X, pady=(15, 5))
        
        # Game modes explanation
        modes = [
            "• AI Opponent: Play against the computer with adjustable difficulty.",
            "• Pass and Play: Play with a friend on the same device."
        ]
        
        for mode in modes:
            tk.Label(
                rules_frame,
                text=mode,
                font=("Arial", 11),
                bg=self.colors["bg_main"],
                fg=self.colors["text_dark"],
                anchor="w"
            ).pack(fill=tk.X, pady=3)
        
        # Close button
        close_btn = ModernButton(
            help_window,
            text="Close",
            command=help_window.destroy,
            bg=self.colors["btn_primary"],
            hover_bg=self.colors["btn_hover"],
            fg=self.colors["text_light"],
            width=100,
            height=35
        )
        close_btn.pack(pady=20)


def main():
    """Main function to start the game."""
    # Enable DPI awareness for better display on high-resolution screens
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass  # Not available on all platforms
    
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()