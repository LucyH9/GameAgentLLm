from experiments.match_runner import play_game
from game.connect4 import PLAYER_X, PLAYER_O
from players.random_player import choose_random_move
from players.heuristic_player import choose_heuristic_move
from players.minimax_player import choose_minimax_move


def run_minimax_vs_random(num_games=10, minimax_as="X", depth=3):
    def minimax_x(board):
        return choose_minimax_move(board, PLAYER_X, depth=depth)

    def minimax_o(board):
        return choose_minimax_move(board, PLAYER_O, depth=depth)

    def random_x(board):
        return choose_random_move(board)

    def random_o(board):
        return choose_random_move(board)

    x_wins = 0
    o_wins = 0
    draws = 0

    for _ in range(num_games):
        if minimax_as == "X":
            result = play_game(minimax_x, random_o, print_game=False)
        else:
            result = play_game(random_x, minimax_o, print_game=False)

        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

    return {
        "matchup": f"Minimax vs Random (Minimax as {minimax_as})",
        "games": num_games,
        "X_wins": x_wins,
        "O_wins": o_wins,
        "draws": draws,
        "depth": depth,
    }


def run_minimax_vs_heuristic(num_games=10, minimax_as="X", depth=3):
    def minimax_x(board):
        return choose_minimax_move(board, PLAYER_X, depth=depth)

    def minimax_o(board):
        return choose_minimax_move(board, PLAYER_O, depth=depth)

    def heuristic_x(board):
        return choose_heuristic_move(board, PLAYER_X, PLAYER_O)

    def heuristic_o(board):
        return choose_heuristic_move(board, PLAYER_O, PLAYER_X)

    x_wins = 0
    o_wins = 0
    draws = 0

    for _ in range(num_games):
        if minimax_as == "X":
            result = play_game(minimax_x, heuristic_o, print_game=False)
        else:
            result = play_game(heuristic_x, minimax_o, print_game=False)

        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

    return {
        "matchup": f"Minimax vs Heuristic (Minimax as {minimax_as})",
        "games": num_games,
        "X_wins": x_wins,
        "O_wins": o_wins,
        "draws": draws,
        "depth": depth,
    }