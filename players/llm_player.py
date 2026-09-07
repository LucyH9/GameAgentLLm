import time
from game.connect4 import get_legal_moves
from llm.prompt_builder import build_move_prompt
from llm.output_parser import parse_move_response


def choose_llm_move(board, player, llm_client, return_debug=False):
    """
    Ask the LLM for a move.
    If the response is invalid or illegal, fall back to the first legal move.

    If return_debug=True, return a tuple:
    (final_move, debug_info)
    """
    #Get the list of currently legal moves.
    legal_moves = get_legal_moves(board)

    #Build the prompt from the current board state and player.
    prompt = build_move_prompt(board, player)

    #Measure how long the LLM takes to respond.
    start_time = time.perf_counter()
    response_text = llm_client.get_chat_response(
        prompt,
        system_message="You are a Connect-4 agent. Return only valid JSON."
    )
    end_time = time.perf_counter()

    #Parse the model's response into a move.
    parsed_move = parse_move_response(response_text)

    #Store debugging information about the response.
    debug_info = {
        "raw_response": response_text,
        "parsed_move": parsed_move,
        "used_fallback": False,
        "fallback_reason": None,
        "latency_seconds": end_time - start_time,
    }

    #Fall back to the first legal move if parsing fails.
    if parsed_move is None:
        debug_info["used_fallback"] = True
        debug_info["fallback_reason"] = "parse_failure"
        final_move = legal_moves[0]

    #Fall back if the parsed move is not legal in the current state.
    elif parsed_move not in legal_moves:
        debug_info["used_fallback"] = True
        debug_info["fallback_reason"] = "illegal_move"
        final_move = legal_moves[0]

    #Otherwise, use the LLM's chosen move.
    else:
        final_move = parsed_move

    #Return debug info if requested.
    if return_debug:
        return final_move, debug_info

    return final_move