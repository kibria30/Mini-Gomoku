"""
Gomoku GUI Implementation

Features:
- Dark scalable background
- Left-aligned text throughout
- Complete game flow with menu, settings, and gameplay
- AI integration with difficulty levels
- Win prediction display
"""

import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QStackedWidget, QMessageBox, QFileDialog, QButtonGroup)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon, QImage
from gomoku_game import GomokuGame
from gomoku_ai import GomokuAI


class GomokuGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("GOMOKU AI")
        self.setMinimumSize(800, 600)

        self.setStyleSheet("""
            QWidget {
                color: white;
            }
            QLabel {
                color: white;
            }
        """)

        # Color palette
        self.COLORS = {
            # Backgrounds
            'bg_dark': '#333333',
            'bg_wood': '#D2B48C',  # Tan wood color
            'bg_panel': '#444444',

            # Text
            'text_light': '#FFFFFF',
            'text_dark': '#000000',

            # Interactive elements
            'button_base': '#444444',
            'button_hover': '#555555',
            'button_border': '#555555',

            # Selection states
            'select_green': '#4CAF50',
            'select_green_hover': '#45A049',
            'select_blue': '#2196F3',
            'select_blue_hover': '#0B7DDA',
            'select_orange': '#FF9800',
            'select_orange_hover': '#E68A00',

            # Game elements
            'stone_black': '#2D2D2D',
            'stone_white': '#FAFAFA',
            'stone_shadow': 'rgba(100, 100, 100, 150)',
            'grid_line': '#966F33',
            'highlight': 'rgba(255, 215, 0, 150)',

            # Top bar
            'top_bar': '#FADCA2',
            'top_bar_border': '#E8C98F',
            'window_control_hover': '#E8C98F'
        }

        # Game state
        self.game = None
        self.ai = None
        self.ai_thinking = False
        self.player_color = 1
        self.board_size = 15
        self.ai_difficulty = 3
        self.pass_and_play = False

        # Initialize UI
        self.init_ui()

        # Load background
        self.background = QPixmap("assets/background.jpg")
        if self.background.isNull():
            self.background = QPixmap(QSize(1, 1))
            self.background.fill(QColor(self.COLORS['bg_dark']))

    def get_color(self, name, alpha=255):
        """Helper to get QColor from palette with optional alpha"""
        color = QColor(self.COLORS[name])
        if alpha != 255:
            color.setAlpha(alpha)
        return color

    def init_ui(self):
        # previously here were some stylesheets
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Stacked widget for views
        self.stacked_widget = QStackedWidget()

        # Create views
        self.menu_view = self.create_menu_view()
        self.settings_view = self.create_settings_view()
        self.game_view = self.create_game_view()

        # Add views to stack
        self.stacked_widget.addWidget(self.menu_view)
        self.stacked_widget.addWidget(self.settings_view)
        self.stacked_widget.addWidget(self.game_view)

        # Main layout
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)

        # Create top bar
        self.create_top_bar()

    def create_top_bar(self):
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(70)
        self.top_bar.setStyleSheet(f"""
            background-color: {self.COLORS['top_bar']};
            border-bottom: 1px solid {self.COLORS['top_bar_border']};
        """)

        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        # Title
        title = QLabel("GOMOKU AI")
        title.setStyleSheet(f"""
            font-size: 24px; 
            font-weight: bold;
            color: {self.COLORS['text_dark']};
        """)
        top_layout.addWidget(title, alignment=Qt.AlignLeft)

        # Window controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)

        for symbol, action in [("—", self.showMinimized),
                               ("□", self.toggle_maximize),
                               ("×", self.close)]:
            btn = QPushButton(symbol)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    font-size: 18px;
                    color: {self.COLORS['text_dark']};
                }}
                QPushButton:hover {{
                    background-color: {self.COLORS['window_control_hover']};
                }}
            """)
            btn.clicked.connect(action)
            controls_layout.addWidget(btn)

        top_layout.addWidget(controls, alignment=Qt.AlignRight)
        self.central_widget.layout().insertWidget(0, self.top_bar)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # below menu is final
    def create_menu_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)  # Center all content
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # Welcome message - Bigger, bolder, and centered
        welcome = QLabel("Welcome to Gomoku AI!")
        welcome.setStyleSheet("""
            QLabel {
                font-size: 42px;
                font-weight: bold;
                color: white;
                padding-bottom: 20px;
            }
        """)
        layout.addWidget(welcome, alignment=Qt.AlignCenter)

        # Start Game button (centered)
        start_btn = QPushButton("Start Game")
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 12px 30px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        start_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_view))
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)

        # Rules button (centered)
        rules_btn = QPushButton("Rules of Gomoku")
        rules_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 18px;
                padding: 12px 30px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        rules_btn.clicked.connect(self.show_rules)
        layout.addWidget(rules_btn, alignment=Qt.AlignCenter)

        return widget

    def show_rules(self):
        rules = """
        <h2>Rules of Gomoku</h2>
        <p>Gomoku is a strategy board game played with black and white stones.</p>
        <p><b>Objective:</b> Be the first to get 5 stones in a row (horizontally, vertically, or diagonally).</p>
        <p><b>Gameplay:</b></p>
        <ul>
            <li>Players alternate turns placing stones of their color</li>
            <li>Black plays first</li>
            <li>Stones are placed on intersections (like Go)</li>
            <li>Once placed, stones cannot be moved</li>
        </ul>
        <p>The game ends when one player forms a line of 5 stones or when the board is full.</p>
        """

        msg = QMessageBox()
        msg.setWindowTitle("Rules of Gomoku")
        msg.setTextFormat(Qt.RichText)
        msg.setText(rules)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #333333;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #444444;
                color: white;
                padding: 5px 10px;
            }
        """)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def create_settings_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet(f"""
            font-size: 14px; 
            border: none; 
            color: {self.COLORS['select_blue']};
        """)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.menu_view))
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Title
        title = QLabel("Game Settings")
        title.setStyleSheet("font-size: 28px;")
        layout.addWidget(title)

        # Board size selection
        size_label = QLabel("Board Size:")
        size_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(size_label)

        size_group = QWidget()
        size_layout = QHBoxLayout(size_group)
        self.size_btns = []

        for size in [10, 15, 19]:
            btn = QPushButton(f"{size}x{size}")
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    padding: 8px;
                    border: 2px solid {self.COLORS['button_border']};
                    border-radius: 5px;
                    min-width: 80px;
                    background-color: {self.COLORS['button_base']};
                    color: {self.COLORS['text_light']};
                }}
                QPushButton:hover {{
                    background-color: {self.COLORS['button_hover']};
                }}
                QPushButton:checked {{
                    background-color: {self.COLORS['select_green']};
                    border-color: {self.COLORS['select_green_hover']};
                }}
            """)
            btn.clicked.connect(lambda _, s=size: self.set_board_size(s))
            size_layout.addWidget(btn)
            self.size_btns.append(btn)

        self.size_btns[1].setChecked(True)
        layout.addWidget(size_group)

        # Game mode selection
        mode_label = QLabel("Game Mode:")
        mode_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(mode_label)

        self.mode_btns = []
        mode_group = QWidget()
        mode_layout = QHBoxLayout(mode_group)

####################################################3
        pass_play = QPushButton("Pass & Play")
        pass_play.setCheckable(True)
        pass_play.setChecked(True)
        pass_play.setStyleSheet(f"""
            QPushButton {{
                padding: 8px;
                border: 2px solid {self.COLORS['button_border']};
                border-radius: 5px;
                min-width: 80px;
                background-color: {self.COLORS['button_base']};
                color: {self.COLORS['text_light']};
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['button_hover']};
            }}
            QPushButton:checked {{
                background-color: {self.COLORS['select_green']};
                border-color: {self.COLORS['select_green_hover']};
            }}
        """)
        pass_play.clicked.connect(self.toggle_ai_settings)
        mode_layout.addWidget(pass_play)
        self.mode_btns.append(pass_play)

        vs_ai = QPushButton("Play Against AI")
        vs_ai.setCheckable(True)
        vs_ai.setStyleSheet(f"""
            QPushButton {{
                padding: 8px;
                border: 2px solid {self.COLORS['button_border']};
                border-radius: 5px;
                min-width: 80px;
                background-color: {self.COLORS['button_base']};
                color: {self.COLORS['text_light']};
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['button_hover']};
            }}
            QPushButton:checked {{
                background-color: {self.COLORS['select_green']};
                border-color: {self.COLORS['select_green_hover']};
            }}
        """)
        vs_ai.clicked.connect(self.toggle_ai_settings)
        mode_layout.addWidget(vs_ai)
        self.mode_btns.append(vs_ai)

        layout.addWidget(mode_group)

        # AI settings (initially hidden)
        self.ai_settings = QWidget()
        ai_layout = QVBoxLayout(self.ai_settings)
        ai_layout.setContentsMargins(0, 0, 0, 0)
        ai_layout.setSpacing(15)

        # Piece selection
        piece_label = QLabel("Your Piece Color:")
        piece_label.setStyleSheet("font-size: 16px;")
        ai_layout.addWidget(piece_label)

        self.piece_btns = []
        piece_group = QWidget()
        piece_layout = QHBoxLayout(piece_group)

        black = QPushButton("Black (First)")
        black.setCheckable(True)
        black.setChecked(True)
        black.setStyleSheet(f"""
            QPushButton {{
                padding: 8px;
                border: 2px solid {self.COLORS['button_border']};
                border-radius: 5px;
                min-width: 80px;
                background-color: {self.COLORS['button_base']};
                color: {self.COLORS['text_light']};
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['button_hover']};
            }}
            QPushButton:checked {{
                background-color: {self.COLORS['select_green']};
                border-color: {self.COLORS['select_green_hover']};
            }}
        """)
        black.clicked.connect(lambda: self.set_player_color(1))
        piece_layout.addWidget(black)
        self.piece_btns.append(black)

        white = QPushButton("White (Second)")
        white.setCheckable(True)
        white.setStyleSheet(f"""
            QPushButton {{
                padding: 8px;
                border: 2px solid {self.COLORS['button_border']};
                border-radius: 5px;
                min-width: 80px;
                background-color: {self.COLORS['button_base']};
                color: {self.COLORS['text_light']};
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['button_hover']};
            }}
            QPushButton:checked {{
                background-color: {self.COLORS['select_green']};
                border-color: {self.COLORS['select_green_hover']};
            }}
        """)
        white.clicked.connect(lambda: self.set_player_color(2))
        piece_layout.addWidget(white)
        self.piece_btns.append(white)

        ai_layout.addWidget(piece_group)

        # Difficulty selection
        diff_label = QLabel("AI Difficulty:")
        diff_label.setStyleSheet("font-size: 16px;")
        ai_layout.addWidget(diff_label)

        self.diff_btns = []
        diff_group = QWidget()
        diff_layout = QHBoxLayout(diff_group)

        for i, diff in enumerate(["Easy", "Normal", "Hard"]):
            btn = QPushButton(diff)
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    padding: 8px;
                    border: 2px solid {self.COLORS['button_border']};
                    border-radius: 5px;
                    min-width: 80px;
                    background-color: {self.COLORS['button_base']};
                    color: {self.COLORS['text_light']};
                }}
                QPushButton:hover {{
                    background-color: {self.COLORS['button_hover']};
                }}
                QPushButton:checked {{
                    background-color: {self.COLORS['select_orange']};
                    border-color: {self.COLORS['select_orange_hover']};
                }}
                QPushButton:checked:hover {{
                    background-color: {self.COLORS['select_orange_hover']};
                }}
            """)
            if i == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda _, d=i + 3: self.set_ai_difficulty(d))
            diff_layout.addWidget(btn)
            self.diff_btns.append(btn)

        ai_layout.addWidget(diff_group)
        layout.addWidget(self.ai_settings)
        self.ai_settings.hide()

        # Start button
        start_btn = QPushButton("Start Game")
        start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLORS['select_green']};
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['select_green_hover']};
            }}
        """)
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn, alignment=Qt.AlignLeft)

        return widget

    def toggle_ai_settings(self):
        sender = self.sender()
        for btn in self.mode_btns:
            btn.setChecked(btn == sender)

        if sender.text() == "Play Against AI":
            self.ai_settings.show()
        else:
            self.ai_settings.hide()

    def set_board_size(self, size):
        self.board_size = size
        for btn in self.size_btns:
            btn.setChecked(btn.text() == f"{size}x{size}")

    def set_player_color(self, color):
        self.player_color = color
        for i, btn in enumerate(self.piece_btns):
            btn.setChecked(i == color - 1)

    def set_ai_difficulty(self, difficulty):
        self.ai_difficulty = difficulty
        for i, btn in enumerate(self.diff_btns):
            btn.setChecked(i == difficulty - 3)

    def create_game_view(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Left side - game board
        self.board_widget = QWidget()
        self.board_widget.setMinimumSize(400, 400)
        self.board_layout = QVBoxLayout(self.board_widget)
        self.board_layout.setAlignment(Qt.AlignCenter)

        # Board display
        self.board_display = QLabel()
        self.board_display.setAlignment(Qt.AlignCenter)
        self.board_layout.addWidget(self.board_display)

        # Win prediction
        self.win_prediction = QLabel(":)")
        self.win_prediction.setStyleSheet("font-size: 16px; margin-top: 20px;")
        self.board_layout.addWidget(self.win_prediction)

        layout.addWidget(self.board_widget, stretch=1)

        # Right side - controls
        controls = QWidget()
        controls.setFixedWidth(200)
        controls_layout = QVBoxLayout(controls)
        controls_layout.setAlignment(Qt.AlignTop)
        controls_layout.setSpacing(15)

        # Game info

        self.game_info = QLabel("Current turn: Black")
        self.game_info.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 500;  /* Semi-bold */
                color: #E0E0E0;   /* Soft white */
                background-color: #424242;  /* Dark gray */
                border: 1px solid #616161;  /* Slightly lighter border */
                border-radius: 4px;
                padding: 6px 12px;
                margin: 8px 0;
                min-width: 180px;
                text-align: center;
            }
        """)
        controls_layout.addWidget(self.game_info)
### fix this
        # Control buttons
        new_game = QPushButton("Start New Game")
        undo = QPushButton("Undo Move")
        abandon = QPushButton("Abandon Game")
        hint = QPushButton("Get Hint")

        for btn in [new_game, undo, abandon, hint]:
            btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.COLORS['select_green']};
                color: white;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
                width: 200px;
                margin-top: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.COLORS['select_green_hover']};
            }}
        """)
            controls_layout.addWidget(btn)

        new_game.clicked.connect(self.reset_game)
        undo.clicked.connect(self.undo_move)
        abandon.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_view))
        hint.clicked.connect(self.get_hint)

        controls_layout.addStretch()
        layout.addWidget(controls)

        return widget

    def start_game(self):
        # Initialize game
        self.game = GomokuGame(self.board_size)
        self.pass_and_play = self.get_selected_mode() == 0  # 0 = Pass & Play

        # Initialize AI only if not in Pass & Play mode
        if not self.pass_and_play:
            self.ai = GomokuAI(max_depth=self.ai_difficulty, player_id=3 - self.player_color)
            if self.player_color == 2:  # AI goes first if player chose white
                self.make_ai_move()

        # Update UI
        self.update_board()
        self.update_game_info()
        self.stacked_widget.setCurrentWidget(self.game_view)

## style here
    def reset_game(self):
        # Confirm with user
        reply = QMessageBox(QMessageBox.Question,
                            'Confirm',
                            'Start a new game? Current game will be lost.',
                            QMessageBox.Yes | QMessageBox.No,
                            self)
        reply.setDefaultButton(QMessageBox.No)

        # Show the dialog but do not block yet
        yes_button = reply.button(QMessageBox.Yes)
        no_button = reply.button(QMessageBox.No)

        # Apply styles directly to buttons
        yes_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #555555;
                border: 1px solid #888888;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)

        no_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #555555;
                border: 1px solid #888888;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)

        # Set overall style for dialog
        reply.setStyleSheet("""
            QMessageBox {
                background-color: #333333;
                color: white;
            }
            QLabel {
                color: white;
            }
        """)

        # Get the response
        result = reply.exec_()
        if result == QMessageBox.Yes:
            self.start_game()

        # if reply == QMessageBox.Yes:
        #     self.start_game()

    def undo_move(self):
        if self.game and not self.ai_thinking:
            if self.ai and len(self.game.move_history) > 0:
                # In AI mode, undo both player and AI moves
                if len(self.game.move_history) > 1 and self.game.move_history[-1][2] == self.ai.player_id:
                    self.game.undo_move()  # Undo AI move
                self.game.undo_move()  # Undo player move
            else:
                self.game.undo_move()

            self.update_board()
            self.update_game_info()

    def get_hint(self):
        if self.game and not self.ai_thinking and self.game.current_player == self.player_color:
            # Use AI to find best move
            best_move = self.ai.choose_move(self.game)
            if best_move:
                row, col = best_move
                self.show_hint(row, col)

    def show_hint(self, row, col):
        # Highlight the suggested move
        self.update_board(highlight=(row, col))
        QTimer.singleShot(2000, self.update_board)  # Remove highlight after 2 seconds

    def make_ai_move(self):
        if self.ai and self.game.current_player == self.ai.player_id and not self.game.game_over:
            self.ai_thinking = True
            self.game_info.setText("AI is thinking...")
            QTimer.singleShot(100, self.process_ai_move)  # Small delay for UI update

    def process_ai_move(self):
        best_move = self.ai.choose_move(self.game)
        if best_move:
            row, col = best_move
            self.game.make_move(row, col)

        self.ai_thinking = False
        self.update_board()
        self.update_game_info()

        # Check if game is over after AI move
        if self.game.game_over:
            self.show_game_result()

    def mousePressEvent(self, event):
        if (self.stacked_widget.currentWidget() == self.game_view
                and not self.ai_thinking
                and self.game
                and not self.game.game_over):

            pos = self.board_display.mapFrom(self, event.pos())
            cell_size = self.board_display.pixmap().width() / self.board_size
            col = int(pos.x() / cell_size)
            row = int(pos.y() / cell_size)

            # For both modes: Check valid move
            if (0 <= row < self.board_size
                    and 0 <= col < self.board_size
                    and self.game.is_valid_move(row, col)):

                # In AI mode, only allow current player's moves
                if not self.pass_and_play and self.game.current_player != self.player_color:
                    return

                if self.game.make_move(row, col):
                    self.update_board()
                    self.update_game_info()

                    if self.game.game_over:
                        self.show_game_result()
                    elif not self.pass_and_play and self.game.current_player == self.ai.player_id:
                        self.make_ai_move()  # Trigger AI move if in AI mode

    def update_board(self, highlight=None):
        if not self.game:
            return

        # Create board image with wood background
        board_size = self.game.board_size
        cell_size = 40
        img_size = board_size * cell_size
        img = QImage(img_size, img_size, QImage.Format_RGB32)  # Changed to RGB32 for opaque background

        # Create painter
        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill with wood color background
        wood_color = QColor(210, 180, 140)  # Light wood color
        painter.fillRect(img.rect(), wood_color)

        # Draw grid lines (darker wood for lines)
        painter.setPen(QColor(150, 120, 80))
        for i in range(board_size):
            painter.drawLine(cell_size // 2, cell_size // 2 + i * cell_size,
                             img_size - cell_size // 2, cell_size // 2 + i * cell_size)
            painter.drawLine(cell_size // 2 + i * cell_size, cell_size // 2,
                             cell_size // 2 + i * cell_size, img_size - cell_size // 2)

        # Draw stones with shadow effect
        stone_shadow = QColor(100, 100, 100, 150)
        for row in range(board_size):
            for col in range(board_size):
                if self.game.board[row, col] == 1:  # Black stone
                    # Shadow
                    painter.setBrush(stone_shadow)
                    painter.drawEllipse(col * cell_size + 4, row * cell_size + 4,
                                        cell_size - 4, cell_size - 4)
                    # Stone
                    painter.setBrush(QColor(45, 45, 45))
                    painter.drawEllipse(col * cell_size + 2, row * cell_size + 2,
                                        cell_size - 4, cell_size - 4)

                elif self.game.board[row, col] == 2:  # White stone
                    # Shadow
                    painter.setBrush(stone_shadow)
                    painter.drawEllipse(col * cell_size + 4, row * cell_size + 4,
                                        cell_size - 4, cell_size - 4)
                    # Stone
                    painter.setBrush(QColor(250, 250, 250))
                    painter.drawEllipse(col * cell_size + 2, row * cell_size + 2,
                                        cell_size - 4, cell_size - 4)

        # Highlight for hints
        if highlight:
            row, col = highlight
            highlight_color = QColor(255, 215, 0, 150)  # Gold with transparency
            painter.setBrush(highlight_color)
            painter.drawEllipse(col * cell_size, row * cell_size,
                                cell_size, cell_size)

        painter.end()
        self.board_display.setPixmap(QPixmap.fromImage(img))

    def update_game_info(self):
        if not self.game:
            return

        # Update turn info
        if self.game.game_over:
            if self.game.winner == 0:
                text = "Game ended in a draw!"
                self.game_info.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                        font-weight: bold;
                        color: #FADCA2;
                        background-color: rgba(70, 70, 70, 200);
                        border: 1px solid #616161;
                        border-radius: 6px;
                        padding: 8px 12px;
                        min-width: 200px;
                        text-align: center;
                    }
                """)
            else:
                winner = "Black" if self.game.winner == 1 else "White"
                text = f"{winner} wins!"
                self.game_info.setStyleSheet(f"""
                    QLabel {{
                        font-size: 18px;
                        font-weight: bold;
                        color: {'#FADCA2' if winner == 'Black' else '#FFFFFF'};
                        background-color: {'rgba(50, 70, 50, 200)' if winner == 'Black' else 'rgba(70, 70, 90, 200)'};
                        border: 1px solid {'#45a049' if winner == 'Black' else '#0b7dda'};
                        border-radius: 6px;
                        padding: 8px 12px;
                        min-width: 200px;
                        text-align: center;
                    }}
                """)
        else:
            current = "Black" if self.game.current_player == 1 else "White"
            if self.pass_and_play:
                text = f"{current}'s turn"
            else:
                text = f"Your turn ({current})" if self.game.current_player == self.player_color else f"AI thinking..."

            self.game_info.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    font-weight: 500;
                    color: #E0E0E0;
                    background-color: #424242;
                    border: 1px solid #616161;
                    border-radius: 4px;
                    padding: 6px 12px;
                    min-width: 180px;
                    text-align: center;
                }}
            """)

        self.game_info.setText(text)

        # Win prediction styling
        if not self.game.game_over and self.ai:
            score = self.ai.evaluate(self.game)
            black_score = 50 + min(45, score // 2000)  # Scale to 5-95%
            white_score = 100 - black_score

            self.win_prediction.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: 500;
                    color: #E0E0E0;
                    background-color: rgba(50, 50, 50, 180);
                    border-radius: 6px;
                    padding: 8px 12px;
                    margin-top: 8px;
                    min-width: 240px;
                    text-align: center;
                }
            """)

            self.win_prediction.setText(
                f"""
                <table cellspacing='0' cellpadding='2'>
                    <tr>
                        <td style='color: #FFFFFF; 
                                  background-color: #2D2D2D;  /* Dark black stone color */
                                  padding: 4px 8px; 
                                  border-radius: 4px 0 0 4px;
                                  font-weight: bold;'>Black</td>
                        <td style='color: #FADCA2;  /* Gold text for visibility */
                                  background-color: #424242;
                                  padding: 0 8px;'>{black_score}%</td>
                        <td style='color: #E0E0E0;
                                  background-color: #424242;
                                  padding: 0 4px;'>-</td>
                        <td style='color: #FADCA2;  /* Gold text for visibility */
                                  background-color: #424242;
                                  padding: 0 8px;'>{white_score}%</td>
                        <td style='color: #000000; 
                                  background-color: #FAFAFA;  /* White stone color */
                                  padding: 4px 8px; 
                                  border-radius: 0 4px 4px 0;
                                  font-weight: bold;'>White</td>
                    </tr>
                </table>
                """
            )

    def show_game_result(self):
        if not self.game or not self.game.game_over:
            return

        if self.game.winner == 0:
            msg = "The game ended in a draw!"
        else:
            winner = "Black" if self.game.winner == 1 else "White"
            msg = f"{winner} wins the game!"

        # Create standard QMessageBox (without frameless flag)
        dialog = QMessageBox()
        dialog.setWindowTitle("Game Over")
        dialog.setText(msg)
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #333333;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #444444;
                color: white;
                padding: 5px 10px;
            }
        """)

        # Add custom buttons
        download_btn = dialog.addButton("Download Board", QMessageBox.ActionRole)
        close_btn = dialog.addButton("Close", QMessageBox.AcceptRole)

        # Connect buttons
        download_btn.clicked.connect(self.download_board)
        close_btn.clicked.connect(dialog.close)

        # Execute dialog
        dialog.exec_()

    def paintEvent(self, event):
        # Paint background
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        ))
        painter.end()

        super().paintEvent(event)

    def download_board(self):
        """Save the current board state as an image file."""
        if not self.game:
            return

        # Create a QPixmap from the board display
        pixmap = self.board_display.pixmap()
        if not pixmap:
            QMessageBox.warning(self, "Error", "No board to save")
            return

        # Get save path from user
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Board Image",
            "",  # Start in current directory
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)"
        )

        if file_path:
            # Ensure file extension matches selected filter
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path += '.png'  # Default to PNG

            # Save the image
            success = pixmap.save(file_path)
            if not success:
                QMessageBox.warning(self, "Error", "Failed to save image")

    def get_selected_mode(self):
        for i, btn in enumerate(self.mode_btns):
            if btn.isChecked():
                return i  # 0 for Pass & Play, 1 for AI
        return 0

    def get_selected_color(self):
        for i, btn in enumerate(self.piece_btns):
            if btn.isChecked():
                return i + 1  # 1 for Black, 2 for White
        return 1

    def get_selected_difficulty(self):
        for i, btn in enumerate(self.diff_btns):
            if btn.isChecked():
                return [3, 5, 7][i]  # Easy=3, Normal=5, Hard=7
        return 3


def main():
    app = QApplication(sys.argv)
    window = GomokuGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()