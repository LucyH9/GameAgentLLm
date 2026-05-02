from game.connect4 import (
    get_legal_moves,
    drop_piece,
    check_winner,
    copy_board,
    COLS,
)


def choose_heuristic_move(board, player, opponent):
    """
    Heuristic move selection:
    1. Take a winning move if available.
    2. Block opponent's winning move if needed.
    3. Prefer center column.
    4. Otherwise pick the first legal move.
    """
    legal_moves = get_legal_moves(board)

    #Can I win right now?
    for move in legal_moves:
        test_board = copy_board(board)
        drop_piece(test_board, move, player)
        if check_winner(test_board, player):
            return move

    #Do I need to block opponent's winning move?
    for move in legal_moves:
        test_board = copy_board(board)
        drop_piece(test_board, move, opponent)
        if check_winner(test_board, opponent):
            return move

    #Prefer center column if available
    center_col = COLS // 2
    if center_col in legal_moves:
        return center_col

    #Otherwise pick the first legal move
    return legal_moves[0]