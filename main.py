from game.connect4 import (
    create_board,
    print_board,
    get_legal_moves,
    drop_piece,
    check_winner,
    is_draw,
    PLAYER_X,
    PLAYER_O,
)

def switch_player(player):
    if player == PLAYER_X:
        return PLAYER_O
    return PLAYER_X

board = create_board()
current_player = PLAYER_X

while True:
    print_board(board)
    print("--------------------------------------------------------------------")
    print(f"Player {current_player}'s turn")
    print("Legal moves:", get_legal_moves(board))

    try:
        col = int(input("Choose a column: "))
    except ValueError:
        print("Please enter a number.")
        continue

    if not drop_piece(board, col, current_player):
        print("Illegal move. Try again.")
        continue

    if check_winner(board, current_player):
        print_board(board)
        print(f"Player {current_player} wins!")
        break

    if is_draw(board):
        print_board(board)
        print("It's a draw!")
        break

    current_player = switch_player(current_player)