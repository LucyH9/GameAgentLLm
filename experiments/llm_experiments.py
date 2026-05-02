from experiments.match_runner import play_game
from experiments.game_csv_logger import append_game_result_to_csv
from game.connect4 import PLAYER_X, PLAYER_O
from players.llm_player import choose_llm_move
from players.random_player import choose_random_move
from players.heuristic_player import choose_heuristic_move


def run_llm_vs_random(client, num_games=3, llm_as="X", log_games=False):
    fallback_counter = {"count": 0}
    latency_tracker = {"total": 0.0, "moves": 0}

    def llm_x(board):
        move, debug = choose_llm_move(board, PLAYER_X, client, return_debug=True)
        if debug["used_fallback"]:
            fallback_counter["count"] += 1
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    def llm_o(board):
        move, debug = choose_llm_move(board, PLAYER_O, client, return_debug=True)
        if debug["used_fallback"]:
            fallback_counter["count"] += 1
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    def random_x(board):
        return choose_random_move(board)

    def random_o(board):
        return choose_random_move(board)

    x_wins = 0
    o_wins = 0
    draws = 0

    for game_num in range(1, num_games + 1):
        fallback_before = fallback_counter["count"]
        latency_before = latency_tracker["total"]
        moves_before = latency_tracker["moves"]

        if llm_as == "X":
            result = play_game(llm_x, random_o, print_game=False)
        else:
            result = play_game(random_x, llm_o, print_game=False)

        fallback_after = fallback_counter["count"]
        latency_after = latency_tracker["total"]
        moves_after = latency_tracker["moves"]

        game_fallbacks = fallback_after - fallback_before
        game_latency = latency_after - latency_before
        game_llm_moves = moves_after - moves_before
        game_avg_latency = game_latency / game_llm_moves if game_llm_moves > 0 else 0.0

        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

        if log_games:
            llm_won = (result["winner"] == llm_as)
            baseline_won = (result["winner"] is not None and result["winner"] != llm_as)

            
            game_row = {
                "matchup": "LLM vs Random",
                "baseline_type": "Random",
                "game_number": game_num,
                "llm_side": llm_as,
                "winner": result["winner"],
                "llm_won": llm_won,
                "baseline_won": baseline_won,
                "draw": result["draw"],
                "illegal_move": result["illegal_move"],
                "fallback_uses_this_game": game_fallbacks,
                "llm_moves_this_game": game_llm_moves,
                "llm_total_latency_seconds": round(game_latency, 4),
                "llm_avg_latency_seconds": round(game_avg_latency, 4),
            }
            append_game_result_to_csv(game_row)

    avg_latency_overall = (
        latency_tracker["total"] / latency_tracker["moves"]
        if latency_tracker["moves"] > 0 else 0.0
    )

    return {
        "matchup": f"LLM vs Random (LLM as {llm_as})",
        "games": num_games,
        "X_wins": x_wins,
        "O_wins": o_wins,
        "draws": draws,
        "fallback_uses": fallback_counter["count"],
        "llm_total_moves": latency_tracker["moves"],
        "llm_total_latency_seconds": round(latency_tracker["total"], 4),
        "llm_avg_latency_seconds": round(avg_latency_overall, 4),
    }


def run_llm_vs_heuristic(client, num_games=3, llm_as="X", log_games=False):
    fallback_counter = {"count": 0}
    latency_tracker = {"total": 0.0, "moves": 0}

    def llm_x(board):
        move, debug = choose_llm_move(board, PLAYER_X, client, return_debug=True)
        if debug["used_fallback"]:
            fallback_counter["count"] += 1
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    def llm_o(board):
        move, debug = choose_llm_move(board, PLAYER_O, client, return_debug=True)
        if debug["used_fallback"]:
            fallback_counter["count"] += 1
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    def heuristic_x(board):
        return choose_heuristic_move(board, PLAYER_X, PLAYER_O)

    def heuristic_o(board):
        return choose_heuristic_move(board, PLAYER_O, PLAYER_X)

    x_wins = 0
    o_wins = 0
    draws = 0

    for game_num in range(1, num_games + 1):
        fallback_before = fallback_counter["count"]
        latency_before = latency_tracker["total"]
        moves_before = latency_tracker["moves"]

        if llm_as == "X":
            result = play_game(llm_x, heuristic_o, print_game=False)
        else:
            result = play_game(heuristic_x, llm_o, print_game=False)

        fallback_after = fallback_counter["count"]
        latency_after = latency_tracker["total"]
        moves_after = latency_tracker["moves"]

        game_fallbacks = fallback_after - fallback_before
        game_latency = latency_after - latency_before
        game_llm_moves = moves_after - moves_before
        game_avg_latency = game_latency / game_llm_moves if game_llm_moves > 0 else 0.0

        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

        if log_games:
            llm_won = (result["winner"] == llm_as)
            baseline_won = (result["winner"] is not None and result["winner"] != llm_as)

            game_row = {
                "matchup": "LLM vs Heuristic",
                "baseline_type": "Heuristic",
                "game_number": game_num,
                "llm_side": llm_as,
                "winner": result["winner"],
                "llm_won": llm_won,
                "baseline_won": baseline_won,
                "draw": result["draw"],
                "illegal_move": result["illegal_move"],
                "fallback_uses_this_game": game_fallbacks,
                "llm_moves_this_game": game_llm_moves,
                "llm_total_latency_seconds": round(game_latency, 4),
                "llm_avg_latency_seconds": round(game_avg_latency, 4),
            }
            append_game_result_to_csv(game_row)

    avg_latency_overall = (
        latency_tracker["total"] / latency_tracker["moves"]
        if latency_tracker["moves"] > 0 else 0.0
    )

    return {
        "matchup": f"LLM vs Heuristic (LLM as {llm_as})",
        "games": num_games,
        "X_wins": x_wins,
        "O_wins": o_wins,
        "draws": draws,
        "fallback_uses": fallback_counter["count"],
        "llm_total_moves": latency_tracker["moves"],
        "llm_total_latency_seconds": round(latency_tracker["total"], 4),
        "llm_avg_latency_seconds": round(avg_latency_overall, 4),
    }