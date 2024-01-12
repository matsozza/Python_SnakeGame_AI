from SnakeBoard import SnakeBoard
from SnakeGame import SnakeGame
from NeuralNetwork import NeuralNetwork
import numpy as np
import time


s_board = SnakeBoard(1)
s_game=SnakeGame(s_board)
s_board.init_board()

next_move = "IDLE"
# Apply next move and recalculate (step) all games
while 1:
    [game_over, state, score] = s_game.step_game(next_move)
  
    next_move = s_game.get_key()     
    # Update graphics of all games
    s_board.clear_board()
    s_board.update_board_elements([s_game])