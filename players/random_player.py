import random
from game.connect4 import get_legal_moves

def choose_random_move(board):
    legal_moves = get_legal_moves(board)
    return random.choice(legal_moves)