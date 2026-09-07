import json


def parse_move_response(response_text):
    """
    Parse an LLM response expected to look like:
    {"move": 3}

    Returns the move as an int if valid, otherwise returns None.
    """
    #Try to convert the response text from JSON into a Python object.
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        return None

    #Reject the response if it does not contain a "move" field.
    if "move" not in data:
        return None

    move = data["move"]

    #Reject the response if the move is not an integer.
    if not isinstance(move, int):
        return None

    #Return the parsed move if it is valid.
    return move