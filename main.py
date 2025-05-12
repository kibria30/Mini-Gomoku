"""
Gomoku Main Module

This is the main entry point for the Gomoku game.
"""

import sys
from console_version import main as run_console
from gomoku_gui import run_gui

def main():
    """Main function to start the game."""
    if len(sys.argv) > 1 and sys.argv[1].lower() == "console":
        run_console()
    else:
        run_gui()

if __name__ == "__main__":
    main()