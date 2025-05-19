# Mini-Gomoku AI

A Gomoku (Five-in-a-row) game with an AI opponent powered by the minimax algorithm with alpha-beta pruning and advanced evaluation heuristics.

## Features

- Play against an AI with adjustable difficulty levels
- Choose from multiple board sizes (10×10, 15×15, 19×19)
- Modern GUI interface built with PyQt5
- Pass & Play mode for two human players
- AI powered by:
  - Minimax algorithm with alpha-beta pruning
  - Iterative deepening for time-limited search
  - Pattern-based evaluation function
  - Transposition table for better performance
  - Move ordering to optimize pruning
- Real-time win predictions
- Get hints from the AI
- Undo moves and download game snapshots

## Requirements

- Python 3.x
- NumPy
- PyQt5

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kibria30/Mini-Gomoku
cd Mini-Gomoku
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Play

Run the main.py file to start the game:

```bash
python3 main.py
```

### Game Modes

- **Play Against AI**: Play against the computer with adjustable difficulty
- **Pass & Play**: Play with a friend on the same computer

### Controls

- Click on the board intersections to place your stones
- Use the "Undo Move" button to take back moves
- Use the "Get Hint" button to get a suggested move from the AI
- The "Start New Game" button resets the current game
- Download button to save the current game state as an image

### Rules

- Black plays first
- The first player to form an unbroken chain of 5 stones in a row (horizontally, vertically, or diagonally) wins
- If the board fills up without a winner, the game is a draw

## Project Structure

- `main.py` - Main entry point
- `gomoku_game.py` - Core game logic
- `gomoku_ai.py` - AI implementation with minimax algorithm
- `gomoku_gui_3.py` - PyQt5-based graphical interface
- `console_version.py` - Text-based console version of the game
