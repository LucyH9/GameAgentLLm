from experiments.match_runner import play_game


def run_tournament(player_x_func, player_o_func, num_games=20):
    results = {
        "X_wins": 0,
        "O_wins": 0,
        "draws": 0,
        "illegal_moves": 0,
    }

    for _ in range(num_games):
        result = play_game(player_x_func, player_o_func, print_game=False)

        if result["illegal_move"]:
            results["illegal_moves"] += 1

        if result["draw"]:
            results["draws"] += 1
        elif result["winner"] == "X":
            results["X_wins"] += 1
        elif result["winner"] == "O":
            results["O_wins"] += 1

    return results