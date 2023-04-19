import numpy as np
import random as rd
import copy


def compress_rtl(input_row):
    """
    This function is responsible for compressing 1D array in right-to-left direction
    [ 16 8 8 4 ] -> [ 16 16 4 0 ]
    It is used in <- (a), ^ (w) case

    Uses 2x1 window to find duplicate values

    Sample steps:
        [ {16 8} 8 4 ] (16 != 8)
        [ 16 {8 8} 4 ] (8 == 8)
        [ 16 {16 8} 4 ]
        [ 16 {16 0} 4 ]
        [ 16 16 4 ]
        [ 16 16 4 0 ]
        [ 16 16 {4 0} ] (4 != 0)

    Args:
        input_row: either row (a) or column (w) from game board

    Returns:
        Compressed array that can be interpreted either horizontally or vertically
    """

    row = input_row
    for id_x, _ in enumerate(row[:3]):
        if row[id_x] == row[id_x + 1]:
            row[id_x] = row[id_x] + row[id_x + 1]
            row[id_x + 1] = 0
            row = np.compress(row, row)
            row = np.append(row, np.zeros(4 - len(row), dtype=int))

    return row


def compress_ltr(input_row):
    """
    This function is responsible for compressing 1D array in left-to-right direction
    [ 16 8 8 4 ] -> [ 0 16 16 4 ]
    It is used in -> (d), v (s) case

    Uses 2x1 window to find duplicate values

    Sample steps:
        [ 16 8 {8 4} ] (8 != 4)
        [ 16 {8 8} 4 ] (8 == 8)
        [ 16 {8 16} 4 ]
        [ 16 {0 16} 4 ]
        [ 16 16 4 ]
        [ 0 16 16 4 ]

    Args:
        input_row: either row (a) or column (w) from game board

    Returns:
        Compressed array that can be interpreted either horizontally or vertically
    """

    for id_x in reversed(range(1, len(input_row))):
        if input_row[id_x] == input_row[id_x - 1]:
            input_row[id_x] = input_row[id_x] + input_row[id_x - 1]
            input_row[id_x - 1] = 0
            input_row = np.compress(input_row, input_row)
            input_row = np.insert(input_row, 0, np.zeros(4 - len(input_row), dtype=int))

    return input_row


def check_transform(game_board):
    """
    This function is responsible for determining if there are any moves possible
    If it is not possible to move - game is lost.

    The algorithm works as follows:
    Duplicate check:
    | x  x  x  | c |
    ----------------
    | v  v  v  | x |
    | v  v  v  | x |
    | v  v  v  | x |
    For each v cell check top neighbour and right neighbour.
    If any pair is equal, then we can perform compression, and we didn't lose.
    Check only remaining c cell for left and bottom neighbour or null value.


    Null check (order of operations):
    |  1    2     3     F |
    | (0)4 (1)5  (2)6   3 |
    |  7   (4)8  (5)9   6 |
    |  F    7     8     9 |
    We start together with duplicate check on (1,0) index.
    We check for null value only two neighbours.
    When the loop terminates, check for null two remaining cells.
    (3,0) and (0,3)

    Args:
        game_board:  2D matrix containing powers of 2

    Returns:
        transformable: boolean set to false if we can't move in any direction
    """

    transformable = False

    # Check if transform is possible
    for idy in range(1, 4):
        for idx in range(0, 3):
            right_neighbour = game_board[idy][idx] == game_board[idy][idx + 1]
            top_neighbour = game_board[idy][idx] == game_board[idy - 1][idx]
            if right_neighbour or top_neighbour or game_board[idy][idx + 1] == 0 or game_board[idy - 1][idx] == 0:
                transformable = True

    # Check remaining corner
    left_neighbour = game_board[0][3] == game_board[1][3]
    bottom_neighbour = game_board[0][3] == game_board[0][2]
    if left_neighbour or bottom_neighbour or game_board[0][3] == 0 or game_board[3][0] == 0:
        transformable = True

    return transformable


def move_left(game_board_input):
    """
    This function is responsible for swiping whole board left
    For each row it first removes null values, then adds new null values to the end of the array
    and compresses neighbouring duplicates.

    Args:
        game_board_input: 2D matrix containing powers of 2

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping left
    """

    game_board = game_board_input
    for idy, each in enumerate(game_board):
        each = np.compress(each, each)
        each = np.append(each, np.zeros(4 - len(each), dtype=int))
        each = compress_rtl(each)
        game_board[idy] = each

    return game_board


def move_right(game_board_input):
    """
    This function is responsible for swiping whole board right
    For each row it first removes null values, then adds new null values to the beginning of the array
    and compresses neighbouring duplicates.

    Args:
        game_board_input: 2D matrix containing powers of 2

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping right
    """

    game_board = game_board_input
    for idy, each in enumerate(game_board):
        each = np.compress(each, each)
        each = np.insert(each, 0, np.zeros(4 - len(each), dtype=int))
        each = compress_ltr(each)
        game_board[idy] = each

    return game_board


def move_up(game_board_input):
    """
    This function is responsible for swiping whole board up
    For each column it first removes null values, then adds new null values to the end of the array
    and compresses neighbouring duplicates.

    Args:
        game_board_input: 2D matrix containing powers of 2

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping up
    """

    game_board = game_board_input
    for idx in range(4):
        col = np.array([game_board[row][idx] for row in range(4)])
        col = np.compress(col, col)
        col = np.append(col, np.zeros(4 - len(col), dtype=int))
        col = compress_rtl(col)

        # Assignment loop
        for row in range(4):
            game_board[row][idx] = col[row]

    return game_board


def move_down(game_board_input):
    """
    This function is responsible for swiping whole board down
    For each column it first removes null values, then adds new null values to the beginning of the array
    and compresses neighbouring duplicates.

    Args:
        game_board_input: 2D matrix containing powers of 2

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping down
    """

    game_board = game_board_input
    for idy in range(4):
        col = np.array([game_board[row][idy] for row in range(4)])
        col = np.compress(col, col)
        col = np.insert(col, 0, np.zeros(4 - len(col), dtype=int))
        col = compress_ltr(col)

        # Assignment loop
        for row in range(0, 4):
            game_board[row][idy] = col[row]

    return game_board


def place_new(game_board_input):
    """
    This function is simply responsible for placing base value (2 for 2048) in an unoccupied place.
    First it maps empty cell's indices into new array "empty" as tuples and then picks a random tuple
    for which contents as indices places base value.

    Args:
        game_board_input: 2D matrix containing powers of 2

    Returns:
        game_board: 2D matrix containing powers of 2 after placing new base value
    """
    game_board = game_board_input
    empty = []

    # Create empty spaces matrix
    for idy, each in enumerate(game_board):
        for idx, cell in enumerate(each):
            if cell == 0:
                empty.append((idy, idx))

    # Put 2 in random place
    point = rd.choice(empty)
    game_board[point[0]][point[1]] = 2

    return game_board


def win_check(game_board):
    """
    Simple Python-specific loop to look for 2048 cell.

    Args:
        game_board: 2D matrix containing powers of 2

    Returns:
        boolean value if there is 2048 cell in the board, false otherwise
    """

    for each in game_board:
        for cell in each:
            if cell == 2048:
                return True

    return False


def transform_matrix(game_board_original, move_dir):
    """
    This function is responsible for transforming matrix by aggregating neighboring duplicates in a certain direction.
    It takes game board, adds 2 in random place and performs compression.

    Args:
        game_board_original: 2D matrix containing powers of 2
        move_dir: string from "wsad" set. Defines swiping direction for board

    Returns:
        check_result: boolean set to false if we can't move in any direction
    """

    game_board = copy.deepcopy(game_board_original)
    check_result = True

    # Compression part
    if move_dir == "a":
        game_board = move_left(game_board)

    elif move_dir == "d":
        game_board = move_right(game_board)

    elif move_dir == "w":
        game_board = move_up(game_board)

    elif move_dir == "s":
        game_board = move_down(game_board)

    # Cannot move in the direction if the result is the same
    if not np.array_equal(game_board_original, game_board):
        game_board = place_new(game_board)

    # Check if transform is possible
    is_playable = check_transform(game_board)
    if not is_playable:
        check_result = is_playable

    # Convert list of ndarrays (they use int32, which is numpy object) to list of lists of ints
    # Required by json.loads()
    game_board = [[int(cell) for cell in arr] for arr in game_board]

    return game_board, check_result, int(np.amax(game_board))
