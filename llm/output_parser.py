import json


def parse_move_response(response_text):
    """
    Parse an LLM response expected to look like:
    {"move": 3}

    Returns the move as an int if valid, otherwise returns None.
    """
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        return None

    if "move" not in data:
        return None

    move = data["move"]

    if not isinstance(move, int):
        return None

    return move