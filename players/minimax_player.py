from game.connect4 import (
    ROWS,
    COLS,
    EMPTY,
    PLAYER_X,
    PLAYER_O,
    check_winner,
    get_legal_moves,
    drop_piece,
    copy_board,
    is_terminal_state,
)

def evaluate_window(window, player):
    """
    Score a group of 4 cells.
    """
    opponent = PLAYER_O if player == PLAYER_X else PLAYER_X
    score = 0

    player_count = window.count(player)
    opponent_count = window.count(opponent)
    empty_count = window.count(EMPTY)

    if player_count == 4:
        score += 100
    elif player_count == 3 and empty_count == 1:
        score += 5
    elif player_count == 2 and empty_count == 2:
        score += 2

    if opponent_count == 3 and empty_count == 1:
        score -= 4

    return score


def score_position(board, player):
    """
    Score the whole board from the perspective of 'player'.
    
    """
    
    opponent = PLAYER_O if player == PLAYER_X else PLAYER_X
    score = 0

    #Strong terminal checks first
    if check_winner(board, player):
        return 100000
    if check_winner(board, opponent):
        return -100000

    #Center column preference
    center_col = COLS // 2
    center_array = [board[row][center_col] for row in range(ROWS)]
    center_count = center_array.count(player)
    score += center_count * 3

    # Horizontal windows
    for row in range(ROWS):
        row_array = board[row]
        for col in range(COLS - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window, player)

    # Vertical windows
    for col in range(COLS):
        col_array = [board[row][col] for row in range(ROWS)]
        for row in range(ROWS - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window, player)

    # Diagonal down-right windows
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [
                board[row][col],
                board[row + 1][col + 1],
                board[row + 2][col + 2],
                board[row + 3][col + 3],
            ]
            score += evaluate_window(window, player)

    # Diagonal up-right windows
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [
                board[row][col],
                board[row - 1][col + 1],
                board[row - 2][col + 2],
                board[row - 3][col + 3],
            ]
            score += evaluate_window(window, player)

    return score

def get_opponent(player):
    return PLAYER_O if player == PLAYER_X else PLAYER_X

def minimax(board, depth, maximizing_player, player):
    """
    Minimax search from the perspective of 'player'.
    
    Returns: (best_move, score)
    """
    legal_moves = get_legal_moves(board)
    opponent = get_opponent(player)

    # Base case
    if depth == 0 or is_terminal_state(board):
        return None, score_position(board, player)

    if maximizing_player:
        best_score = float("-inf")
        best_move = legal_moves[0]

        for move in legal_moves:
            temp_board = copy_board(board)
            drop_piece(temp_board, move, player)

            _, score = minimax(temp_board, depth - 1, False, player)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move, best_score

    else:
        best_score = float("inf")
        best_move = legal_moves[0]

        for move in legal_moves:
            temp_board = copy_board(board)
            drop_piece(temp_board, move, opponent)

            _, score = minimax(temp_board, depth - 1, True, player)

            if score < best_score:
                best_score = score
                best_move = move

        return best_move, best_score
    
def choose_minimax_move(board, player, depth=3):
    """
    Return the best move found by minimax.
    """
    move, _ = minimax(board, depth, True, player)
    return move