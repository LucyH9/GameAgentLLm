from experiments.match_runner import play_game
from game.connect4 import PLAYER_X, PLAYER_O
from players.random_player import choose_random_move
from players.heuristic_player import choose_heuristic_move
from players.minimax_player import choose_minimax_move


def run_minimax_vs_random(num_games=10, minimax_as="X", depth=3):
    #Minimax player when controlling X.
    def minimax_x(board):
        return choose_minimax_move(board, PLAYER_X, depth=depth)

    #Minimax player when controlling O.
    def minimax_o(board):
        return choose_minimax_move(board, PLAYER_O, depth=depth)

    #Random player when controlling X.
    def random_x(board):
        return choose_random_move(board)

    #Random player when controlling O.
    def random_o(board):
        return choose_random_move(board)

    #Store final game outcomes.
    x_wins = 0
    o_wins = 0
    draws = 0

    #Run the requested number of games.
    for _ in range(num_games):
        #Run one game with the correct side assignment.
        if minimax_as == "X":
            result = play_game(minimax_x, random_o, print_game=False)
        else:
            result = play_game(random_x, minimax_o, print_game=False)

        #Update win/draw counters.
        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

    #Return the final summary for the full batch.
    return {
        "matchup": f"Minimax vs Random (Minimax as {minimax_as})",
        "games": num_games,
        "X_wins": x_wins,
        "O_wins": o_wins,
        "draws": draws,
        "depth": depth,
    }


def run_minimax_vs_heuristic(num_games=10, minimax_as="X", depth=3):
    #Minimax player when controlling X.
    def minimax_x(board):
        return choose_minimax_move(board, PLAYER_X, depth=depth)

    #Minimax player when controlling O.
    def minimax_o(board):
        return choose_minimax_move(board, PLAYER_O, depth=depth)

    #Heuristic player when controlling X.
    def heuristic_x(board):
        return choose_heuristic_move(board, PLAYER_X, PLAYER_O)

    #Heuristic player when controlling O.
    def heuristic_o(board):
        return choose_heuristic_move(board, PLAYER_O, PLAYER_X)

    #Store final game outcomes.
    x_wins = 0
    o_wins = 0
    draws = 0

    #Run the requested number of games.
    for _ in range(num_games):
        #Run one game with the correct side assignment.
        if minimax_as == "X":
            result = play_game(minimax_x, heuristic_o, print_game=False)
        else:
            result = play_game(heuristic_x, minimax_o, print_game=False)

        #Update win/draw counters.
        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

    #Return the final summary for the full batch.
    return {
        "matchup": f"Minimax vs Heuristic (Minimax as {minimax_as})",
        "games": num_games,
        "X_wins": x_wins,
        "O_wins": o_wins,
        "draws": draws,
        "depth": depth,
    }