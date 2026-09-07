#Import everything that I need
from experiments.match_runner import play_game
from experiments.game_csv_logger import append_game_result_to_csv
from game.connect4 import PLAYER_X, PLAYER_O
from players.llm_player import choose_llm_move
from players.random_player import choose_random_move
from players.heuristic_player import choose_heuristic_move
from players.minimax_player import choose_minimax_move



def run_llm_vs_minimax(client, num_games=3, llm_as="X", depth=3, log_games=False):
    #Track how many times the LLM needed a fallback action.
    fallback_counter = {"count": 0}

    #Track total LLM latency and total number of LLM moves.
    latency_tracker = {"total": 0.0, "moves": 0}

    #LLM player when controlling X.
    def llm_x(board):
        move, debug = choose_llm_move(board, PLAYER_X, client, return_debug=True)

        #Count fallback usage if the LLM output was invalid.
        if debug["used_fallback"]:
            fallback_counter["count"] += 1

        #Add this move's latency to the running total.
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    #LLM player when controlling O.
    def llm_o(board):
        move, debug = choose_llm_move(board, PLAYER_O, client, return_debug=True)

        #Count fallback usage if the LLM output was invalid.
        if debug["used_fallback"]:
            fallback_counter["count"] += 1

        #Add this move's latency to the running total.
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    #Minimax player when controlling X.
    def minimax_x(board):
        return choose_minimax_move(board, PLAYER_X, depth=depth)

    #Minimax player when controlling O.
    def minimax_o(board):
        return choose_minimax_move(board, PLAYER_O, depth=depth)

    #Store final game outcomes.
    x_wins = 0
    o_wins = 0
    draws = 0

    #Run the requested number of games.
    for game_num in range(1, num_games + 1):
        # Save counters before this game starts so this game's values can be isolated later.
        fallback_before = fallback_counter["count"]
        latency_before = latency_tracker["total"]
        moves_before = latency_tracker["moves"]

        # un one game with the correct side assignment.
        if llm_as == "X":
            result = play_game(llm_x, minimax_o, print_game=False)
        else:
            result = play_game(minimax_x, llm_o, print_game=False)

        #Save counters after the game ends.
        fallback_after = fallback_counter["count"]
        latency_after = latency_tracker["total"]
        moves_after = latency_tracker["moves"]

        #Compute this game's fallback usage, latency, and LLM move count.
        game_fallbacks = fallback_after - fallback_before
        game_latency = latency_after - latency_before
        game_llm_moves = moves_after - moves_before
        game_avg_latency = game_latency / game_llm_moves if game_llm_moves > 0 else 0.0

        #Update win/draw counters.
        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

        #Optionally log per-game results to CSV.
        if log_games:
            llm_won = (result["winner"] == llm_as)
            baseline_won = (result["winner"] is not None and result["winner"] != llm_as)

            game_row = {
                "matchup": "LLM vs Minimax",
                "baseline_type": "Minimax",
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

    #Compute average latency across all LLM moves in the batch.
    avg_latency_overall = (
        latency_tracker["total"] / latency_tracker["moves"]
        if latency_tracker["moves"] > 0 else 0.0
    )

    #Return the final summary for the full batch.
    return {
        "matchup": f"LLM vs Minimax (LLM as {llm_as})",
        "games": num_games,
        "X_wins": x_wins,
        "O_wins": o_wins,
        "draws": draws,
        "fallback_uses": fallback_counter["count"],
        "llm_total_moves": latency_tracker["moves"],
        "llm_total_latency_seconds": round(latency_tracker["total"], 4),
        "llm_avg_latency_seconds": round(avg_latency_overall, 4),
        "depth": depth,
    }


def run_llm_vs_random(client, num_games=3, llm_as="X", log_games=False):
    #Track how many times the LLM needed a fallback action.
    fallback_counter = {"count": 0}

    #Track total LLM latency and total number of LLM moves.
    latency_tracker = {"total": 0.0, "moves": 0}

    #LLM player when controlling X.
    def llm_x(board):
        move, debug = choose_llm_move(board, PLAYER_X, client, return_debug=True)

        #Count fallback usage if the LLM output was invalid.
        if debug["used_fallback"]:
            fallback_counter["count"] += 1

        # Add this move's latency to the running total.
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    #LLM player when controlling O.
    def llm_o(board):
        move, debug = choose_llm_move(board, PLAYER_O, client, return_debug=True)

        #Count fallback usage if the LLM output was invalid.
        if debug["used_fallback"]:
            fallback_counter["count"] += 1

        #Add this move's latency to the running total.
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

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
    for game_num in range(1, num_games + 1):
        # Save counters before this game starts so this game's values can be isolated later.
        fallback_before = fallback_counter["count"]
        latency_before = latency_tracker["total"]
        moves_before = latency_tracker["moves"]

        #Run one game with the correct side assignment.
        if llm_as == "X":
            result = play_game(llm_x, random_o, print_game=False)
        else:
            result = play_game(random_x, llm_o, print_game=False)

        #Save counters after the game ends.
        fallback_after = fallback_counter["count"]
        latency_after = latency_tracker["total"]
        moves_after = latency_tracker["moves"]

        #Compute this game's fallback usage, latency, and LLM move count.
        game_fallbacks = fallback_after - fallback_before
        game_latency = latency_after - latency_before
        game_llm_moves = moves_after - moves_before
        game_avg_latency = game_latency / game_llm_moves if game_llm_moves > 0 else 0.0

        #Update win/draw counters.
        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

        #Optionally log per-game results to CSV.
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

    #Compute average latency across all LLM moves in the batch.
    avg_latency_overall = (
        latency_tracker["total"] / latency_tracker["moves"]
        if latency_tracker["moves"] > 0 else 0.0
    )

    #Return the final summary for the full batch.
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
    #Track how many times the LLM needed a fallback action.
    fallback_counter = {"count": 0}

    #Track total LLM latency and total number of LLM moves.
    latency_tracker = {"total": 0.0, "moves": 0}

    #LLM player when controlling X.
    def llm_x(board):
        move, debug = choose_llm_move(board, PLAYER_X, client, return_debug=True)

        #Count fallback usage if the LLM output was invalid.
        if debug["used_fallback"]:
            fallback_counter["count"] += 1

        #Add this move's latency to the running total.
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

    #LLM player when controlling O.
    def llm_o(board):
        move, debug = choose_llm_move(board, PLAYER_O, client, return_debug=True)

        #Count fallback usage if the LLM output was invalid.
        if debug["used_fallback"]:
            fallback_counter["count"] += 1

        #Add this move's latency to the running total.
        latency_tracker["total"] += debug["latency_seconds"]
        latency_tracker["moves"] += 1
        return move

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
    for game_num in range(1, num_games + 1):
        # Save counters before this game starts so this game's values can be isolated later.
        fallback_before = fallback_counter["count"]
        latency_before = latency_tracker["total"]
        moves_before = latency_tracker["moves"]

        #Run one game with the correct side assignment.
        if llm_as == "X":
            result = play_game(llm_x, heuristic_o, print_game=False)
        else:
            result = play_game(heuristic_x, llm_o, print_game=False)

        #Save counters after the game ends.
        fallback_after = fallback_counter["count"]
        latency_after = latency_tracker["total"]
        moves_after = latency_tracker["moves"]

        #Compute this game's fallback usage, latency, and LLM move count.
        game_fallbacks = fallback_after - fallback_before
        game_latency = latency_after - latency_before
        game_llm_moves = moves_after - moves_before
        game_avg_latency = game_latency / game_llm_moves if game_llm_moves > 0 else 0.0

        #Update win/draw counters.
        if result["draw"]:
            draws += 1
        elif result["winner"] == "X":
            x_wins += 1
        elif result["winner"] == "O":
            o_wins += 1

        #Optionally log per-game results to CSV.
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

    #Compute average latency across all LLM moves in the batch.
    avg_latency_overall = (
        latency_tracker["total"] / latency_tracker["moves"]
        if latency_tracker["moves"] > 0 else 0.0
    )

    #Return the final summary for the full batch.
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