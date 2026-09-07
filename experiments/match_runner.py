
#Import needed objects
from game.connect4 import (
    create_board,
    print_board,
    drop_piece,
    check_winner,
    is_draw,
    PLAYER_X,
    PLAYER_O,
)


def play_game(player_x_func, player_o_func, print_game=False):
    """
    Run one full game of Connect-4.

    player_x_func(board) -> move
    player_o_func(board) -> move

    Returns a dictionary with the result.
    """
    board = create_board()
    current_player = PLAYER_X

    while True:
        if print_game:
            print_board(board)

        if current_player == PLAYER_X:
            move = player_x_func(board)
        else:
            move = player_o_func(board)

        success = drop_piece(board, move, current_player)

        if not success:
            #This should not happen for your random/heuristic players,
            #but we handle it anyway just in case :D
            winner = PLAYER_O if current_player == PLAYER_X else PLAYER_X

            if print_game:
                print(f"Illegal move by {current_player}: {move}")
                print(f"Player {winner} wins by forfeit.")

            return {
                "winner": winner,
                "draw": False,
                "illegal_move": True,
                "illegal_player": current_player,
                "final_board": board,
            }

        if check_winner(board, current_player):
            if print_game:
                print_board(board)
                print(f"Player {current_player} wins!")

            return {
                "winner": current_player,
                "draw": False,
                "illegal_move": False,
                "illegal_player": None,
                "final_board": board,
            }

        if is_draw(board):
            if print_game:
                print_board(board)
                print("It's a draw!")

            return {
                "winner": None,
                "draw": True,
                "illegal_move": False,
                "illegal_player": None,
                "final_board": board,
            }

        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X