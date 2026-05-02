from game.connect4 import get_legal_moves


def board_to_string(board):
    """Convert the board into a readable multiline string."""
    lines = []
    for row in board:
        lines.append(" ".join(row))
    lines.append("0 1 2 3 4 5 6")
    return "\n".join(lines)


def build_move_prompt(board, player):
    """
    Build a prompt asking the LLM to choose one legal move in JSON format.
    """
    legal_moves = get_legal_moves(board)
    board_text = board_to_string(board)

    prompt = f"""You are playing Connect-4.

You are player {player}.

Here is the current board:
{board_text}

Legal moves: {legal_moves}

Choose the best legal move.

Return ONLY valid JSON in this exact format:
{{"move": <column_number>}}

Do not include any explanation or extra text.
"""
    return prompt