from random import choice
from copy import deepcopy


def print_game_field(game_list):
    """print game board"""
    sp = (f'---------\n'
          f'| {game_list[0][2]} {game_list[1][2]} {game_list[2][2]} |\n'
          f'| {game_list[0][1]} {game_list[1][1]} {game_list[2][1]} |\n'
          f'| {game_list[0][0]} {game_list[1][0]} {game_list[2][0]} |\n'
          f'---------')
    print(sp)


def check_game_move(game_list, move):
    """Check if a move is available"""
    if game_list[move[0]][move[1]] == ' ':
        return True
    else:
        return False


def possible_moves(game_list):
    """Makes a list of possible moves."""
    possible_moves_ = []
    for row in range(3):
        for col in range(3):
            if check_game_move(game_list, [row, col]):
                possible_moves_.append([row, col])
    return possible_moves_


def win(game_list, player):
    """Victory Check"""
    for i in range(3):
        if game_list[i][0] == game_list[i][1] == game_list[i][2] == player:
            return True
        elif game_list[0][i] == game_list[1][i] == game_list[2][i] == player:
            return True
    if game_list[0][0] == game_list[1][1] == game_list[2][2] == player:
        return True
    elif game_list[0][2] == game_list[1][1] == game_list[2][0] == player:
        return True
    else:
        return False


def check_game_over(game_list):
    if win(game_list, "X") or win(game_list, "O") or possible_moves(game_list) == []:
        return True
    return False


def evaluate_board(game_list, player):
    if player == "O":
        second_player = "X"
    else:
        second_player = "O"
    if win(game_list, player):
        return 1
    elif win(game_list, second_player):
        return -1
    else:
        return 0


def minimax(game_list, is_max, player):
    if player == "O":
        second_player = "X"
    else:
        second_player = "O"
    if check_game_over(game_list):
        return ['', evaluate_board(game_list, player)]
    best_move = ""
    if is_max == True:
        best_value = - float("Inf")
        symbol = player
    else:
        best_value = float("Inf")
        symbol = second_player

    for move in possible_moves(game_list):
        new_game_list = deepcopy(game_list)
        new_game_list[move[0]][move[1]] = symbol
        value = minimax(new_game_list, not is_max, player)
        if is_max and value[1] > best_value:
            best_value = value[1]
            best_move = move
        elif not is_max and value[1] < best_value:
            best_value = value[1]
            best_move = move

    return [best_move, best_value]


def user(game_list, player):
    """Validated user input"""
    while True:
        coordinates = input('Enter the coordinates: ').split(" ")
        try:
            coordinates[0] = int(coordinates[0]) - 1
            coordinates[1] = int(coordinates[1]) - 1
            if coordinates[0] < 0 or coordinates[0] > 2 or coordinates[1] < 0 or coordinates[1] > 2:
                print('Coordinates should be from 1 to 3!')
                continue
            elif not check_game_move(game_list, [coordinates[0], coordinates[1]]):
                print('This cell is occupied! Choose another one!')
                continue
            else:
                return (coordinates, player)
        except ValueError:
            print('You should enter numbers!')
            continue


def easy_ai(game_list, player):
    """Easy game level. AI selects a random cell from possible """
    return (choice(possible_moves(game_list)), player)


def medium_ai(game_list, player):
    """Medium game level
    If it can win in one move (if it has two in a row), it places a third to get three in a row and win.
    If the opponent can win in one move, it plays the third itself to block the opponent to win.
    Otherwise, it makes a random move."""
    if player == "O":
        second_player = "X"
    else:
        second_player = "O"
    possible_moves_ = possible_moves(game_list)
    for i in possible_moves_:
        possible_game_list = deepcopy(game_list)
        possible_game_list[i[0]][i[1]] = player
        if win(possible_game_list, player):
            return (i, player)
    for i in possible_moves_:
        possible_game_list = deepcopy(game_list)
        possible_game_list[i[0]][i[1]] = second_player
        if win(possible_game_list, second_player):
            return (i, player)
    return easy_ai(game_list, player)


def hard_ai(game_list, player):
    """Medium game level. Use minimax"""
    coordinates = minimax(game_list, True, player)[0]
    return (coordinates, player)


def user_game(game_list, player):
    player = user(game_list, player)
    game_list[player[0][0]][player[0][1]] = player[1]
    print_game_field(game_list)
    if win(game_list, player[1]):
        return f"{player[1]} wins"
    elif check_game_over(game_list):
        return 'Draw'
    return True


def game(player_role, second_player_role):
    game_list = [[' ', ' ', ' '], [' ', ' ', ' '], [" ", " ", " "]]
    print_game_field(game_list)
    while True:
        if player_role == 'user':
            player = user(game_list, "X")
        elif player_role == 'easy':
            print('Making move level "easy"')
            player = easy_ai(game_list, "X")
        elif player_role == 'medium':
            print('Making move level "medium"')
            player = medium_ai(game_list, 'X')
        elif player_role == "hard":
            print('Making move level "hard"')
            if len(possible_moves(game_list)) == 9:
                player = ([1, 1], 'X')
            else:
                player = hard_ai(game_list, 'X')

        game_list[player[0][0]][player[0][1]] = player[1]
        print_game_field(game_list)
        if win(game_list, player[1]):
            print(f"{player[1]} wins")
            break
        elif check_game_over(game_list):
            print('Draw')
            break

        if second_player_role == 'user':
            second_player = user(game_list, "O")
        elif second_player_role == 'easy':
            print('Making move level "easy"')
            second_player = easy_ai(game_list, "O")
        elif second_player_role == 'medium':
            print('Making move level "medium"')
            second_player = medium_ai(game_list, 'O')
        elif second_player_role == "hard":
            print('Making move level "hard"')
            second_player = hard_ai(game_list, 'O')

        game_list[second_player[0][0]][second_player[0][1]] = second_player[1]
        print_game_field(game_list)
        if win(game_list, second_player[1]):
            print(f"{second_player[1]} wins")
            break
        elif check_game_over(game_list):
            print('Draw')

lvl = ('user','easy','medium','hard')
while True:
    action = input('Input command: ')
    if action == 'exit':
        break
    else:
        action = action.split(' ')
        if len(action) < 3 or action[0] != 'start' or action[1] not in lvl or action[2] not in lvl:
            print('Bad parameters!')
        else:
            game(action[1], action[2])
