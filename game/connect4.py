ROWS = 6
COLS = 7
EMPTY = "."
PLAYER_X = "X"
PLAYER_O = "O"


def is_terminal_state(board):
    """Return True if the game is over by win or draw."""
    return (
        check_winner(board, PLAYER_X)
        or check_winner(board, PLAYER_O)
        or is_draw(board)
    )

def create_board():
    """Create and return an empty Connect-4 board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board in a readable format."""
    print()
    for row in board:
        print(" ".join(row))
    print("0 1 2 3 4 5 6")
    print()


def get_legal_moves(board):
    """Return a list of columns where a piece can still be dropped."""
    legal_moves = []

    for col in range(COLS):
        if board[0][col] == EMPTY:
            legal_moves.append(col)

    return legal_moves

def drop_piece(board, col, player):
    """
    Drop a piece into a column.
    Returns True if successful, False if the move is illegal.
    """
    if col < 0 or col >= COLS:
        return False

    if board[0][col] != EMPTY:
        return False

    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True
    return False

#Checks for wincon
def check_winner(board, player):
    """Return True if the given player has 4 in a row."""
    
    # Horizontal check
    for row in range(ROWS):
        #test
        for col in range(COLS - 3):
            if (
                board[row][col] == player
                and board[row][col + 1] == player
                and board[row][col + 2] == player
                and board[row][col + 3] == player
            ):
                return True

    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (
                board[row][col] == player
                and board[row + 1][col] == player
                and board[row + 2][col] == player
                and board[row + 3][col] == player
            ):
                return True

    # Diagonal down-right check
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (
                board[row][col] == player
                and board[row + 1][col + 1] == player
                and board[row + 2][col + 2] == player
                and board[row + 3][col + 3] == player
            ):
                return True

    # Diagonal up-right check
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == player
                and board[row - 1][col + 1] == player
                and board[row - 2][col + 2] == player
                and board[row - 3][col + 3] == player
            ):
                return True

    return False


#Draw condition
def is_draw(board):
    """Return True if the board is full."""
    return len(get_legal_moves(board)) == 0

#helper method to copy the board
def copy_board(board):
    """Return a deep copy of the board."""
    return [row[:] for row in board]