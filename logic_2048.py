import random as rd
import numpy as np
import copy


def compress_rtl(row, total_score):
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
        row: either row (a) or column (w) from game board
        total_score: player's score taken to add merged values

    Returns:
        row: compressed array that can be interpreted either horizontally or vertically
        score: player's score
    """

    score = total_score
    for id_x in np.arange(0, 3):
        if row[id_x] == row[id_x + 1]:
            score += row[id_x] + row[id_x + 1]
            row[id_x] = row[id_x] + row[id_x + 1]
            row[id_x + 1] = 0
            row = np.compress(row, row)
            row = np.append(row, np.zeros(4 - len(row), dtype=int))

    return row, score


def compress_ltr(row, total_score):
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
        row: either row (a) or column (w) from game board
        total_score: player's score taken to add merged values

    Returns:
        row: compressed array that can be interpreted either horizontally or vertically
        score:  player's score
    """

    score = total_score
    for id_x in reversed(range(1, len(row))):
        if row[id_x] == row[id_x - 1]:
            score += row[id_x] + row[id_x - 1]
            row[id_x] = row[id_x] + row[id_x - 1]
            row[id_x - 1] = 0
            row = np.compress(row, row)
            row = np.insert(row, 0, np.zeros(4 - len(row), dtype=int))

    return row, score


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
    for idy in np.arange(1, 4):
        for idx in np.arange(0, 3):
            right_neighbour = game_board[idy][idx] == game_board[idy][idx + 1]
            top_neighbour = game_board[idy][idx] == game_board[idy - 1][idx]
            if (
                right_neighbour
                or top_neighbour
                or game_board[idy][idx + 1] == 0
                or game_board[idy - 1][idx] == 0
            ):
                transformable = True

    # Check remaining corner
    left_neighbour = game_board[0][3] == game_board[1][3]
    bottom_neighbour = game_board[0][3] == game_board[0][2]
    if (
        left_neighbour
        or bottom_neighbour
        or game_board[0][3] == 0
        or game_board[3][0] == 0
    ):
        transformable = True

    return transformable


def move_left(game_board, total_score):
    """
    This function is responsible for swiping whole board left
    For each row it first removes null values, then adds new null values to the end of the array
    and compresses neighbouring duplicates.

    Args:
        game_board: 2D matrix containing powers of 2
        total_score: player's score taken to add merged values

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping left
        score:  player's score
        is_changed: boolean telling whether there has been any change in row/column
    """

    score = total_score
    is_changed = False

    for idy, each in enumerate(game_board):
        if not is_changed:
            each_before = copy.deepcopy(each)
            each = np.compress(each, each)
            each = np.append(each, np.zeros(4 - len(each), dtype=int))
            each, score = compress_rtl(each, score)
            game_board[idy] = each

            if not np.array_equal(each_before, each):
                is_changed = True
        else:
            each = np.compress(each, each)
            each = np.append(each, np.zeros(4 - len(each), dtype=int))
            each, score = compress_rtl(each, score)
            game_board[idy] = each

    return game_board, score, is_changed


def move_right(game_board, total_score):
    """
    This function is responsible for swiping whole board right
    For each row it first removes null values, then adds new null values to the beginning of the array
    and compresses neighbouring duplicates.

    Args:
        game_board: 2D matrix containing powers of 2
        total_score:  player's score taken to add merged values

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping right
        score: player's score
        is_changed: boolean telling whether there has been any change in row/column
    """

    score = total_score
    is_changed = False

    for idy, each in enumerate(game_board):
        if not is_changed:
            each_before = copy.deepcopy(each)
            each = np.compress(each, each)
            each = np.insert(each, 0, np.zeros(4 - len(each), dtype=int))
            each, score = compress_ltr(each, score)
            game_board[idy] = each

            if not np.array_equal(each_before, each):
                is_changed = True
        else:
            each = np.compress(each, each)
            each = np.insert(each, 0, np.zeros(4 - len(each), dtype=int))
            each, score = compress_ltr(each, score)
            game_board[idy] = each

    return game_board, score, is_changed


def move_up(game_board, total_score):
    """
    This function is responsible for swiping whole board up
    For each column it first removes null values, then adds new null values to the end of the array
    and compresses neighbouring duplicates.

    Args:
        game_board: 2D matrix containing powers of 2
        total_score: player's score taken to add merged values

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping up
        score: player's score
        is_changed: boolean telling whether there has been any change in row/column
    """

    score = total_score
    is_changed = False

    for idx in np.arange(4):
        if not is_changed:
            col = np.array([game_board[row][idx] for row in np.arange(4)])
            col_before = copy.deepcopy(col)

            col = np.compress(col, col)
            col = np.append(col, np.zeros(4 - len(col), dtype=int))
            col, score = compress_rtl(col, score)

            # Assignment loop
            for row in np.arange(4):
                game_board[row][idx] = col[row]

            if not np.array_equal(col_before, col):
                is_changed = True
        else:
            col = np.array([game_board[row][idx] for row in np.arange(4)])
            col = np.compress(col, col)
            col = np.append(col, np.zeros(4 - len(col), dtype=int))
            col, score = compress_rtl(col, score)

            # Assignment loop
            for row in np.arange(4):
                game_board[row][idx] = col[row]

    return game_board, score, is_changed


def move_down(game_board, total_score):
    """
    This function is responsible for swiping whole board down
    For each column it first removes null values, then adds new null values to the beginning of the array
    and compresses neighbouring duplicates.

    Args:
        game_board: 2D matrix containing powers of 2
        total_score: player's score taken to add merged values

    Returns:
        game_board: 2D matrix containing powers of 2 after swiping down
        score: player's score
        is_changed: boolean telling whether there has been any change in row/column
    """

    score = total_score
    is_changed = False

    for idy in np.arange(4):
        if not is_changed:
            col = np.array([game_board[row][idy] for row in np.arange(4)])
            col_before = copy.deepcopy(col)

            col = np.compress(col, col)
            col = np.insert(col, 0, np.zeros(4 - len(col), dtype=int))
            col, score = compress_ltr(col, score)

            # Assignment loop
            for row in np.arange(0, 4):
                game_board[row][idy] = col[row]

            if not np.array_equal(col_before, col):
                is_changed = True
        else:
            col = np.array([game_board[row][idy] for row in np.arange(4)])
            col = np.compress(col, col)
            col = np.insert(col, 0, np.zeros(4 - len(col), dtype=int))
            col, score = compress_ltr(col, score)

            # Assignment loop
            for row in np.arange(0, 4):
                game_board[row][idy] = col[row]

    return game_board, score, is_changed


def place_new(game_board):
    """
    This function is simply responsible for placing base value (2 for 2048) in an unoccupied place.
    First it maps empty cell's indices into new array "empty" as tuples and then picks a random tuple
    for which contents as indices places base value.

    Args:
        game_board: 2D matrix containing powers of 2

    Returns:
        game_board: 2D matrix containing powers of 2 after placing new base value
    """

    empty_indices = np.argwhere(game_board == 0)

    # Put 2 in random place with 90% of chance and 4 with 10% of chance
    point = rd.choice(empty_indices)
    game_board[point[0]][point[1]] = np.random.choice([2, 4], p=[0.9, 0.1])

    return game_board


def win_check(game_board):
    """
    Simple Python-specific loop to look for 2048 cell.

    Args:
        game_board: 2D matrix containing powers of 2

    Returns:
        boolean value if there is 2048 cell in the board, false otherwise
    """

    return np.any(game_board == 32)


def transform_matrix(game_board, move_dir, total_score, ui_enable):
    """
    This function is responsible for transforming matrix by aggregating neighboring duplicates in a certain direction.
    It takes game board, adds 2 in random place and performs compression.

    Args:
        game_board: 2D matrix containing powers of 2
        move_dir: string from "wsad" set. Defines swiping direction for board
        total_score: player's score calculated as a sum of merged cell's value's
        ui_enable: boolean telling whether this function should return Python's list for Web game (True) or ndarray for ML

    Returns:
        game_board: changed 2D game table
        check_result: boolean set to false if we can't move in any direction
        int(np.amax(game_board)): biggest value in the set (needed for UI)
        score: player's changed total score
        is_changed: boolean telling whether the board has been changed (needed for ML)
    """

    score = total_score
    check_result = True
    is_changed = False

    # Compression part
    if move_dir == "a":
        game_board, score, change = move_left(game_board, score)
        is_changed = change

    elif move_dir == "d":
        game_board, score, change = move_right(game_board, score)
        is_changed = change

    elif move_dir == "w":
        game_board, score, change = move_up(game_board, score)
        is_changed = change

    elif move_dir == "s":
        game_board, score, change = move_down(game_board, score)
        is_changed = change

    # Cannot move in the direction if the result is the same
    if is_changed:
        game_board = place_new(game_board)

    # Check if transform is possible
    is_playable = check_transform(game_board)
    if not is_playable:
        check_result = is_playable

    # Convert list of ndarrays (they use int32, which is numpy object) to list of lists of ints
    # Required by json.loads()
    if ui_enable:
        game_board = [[int(cell) for cell in arr] for arr in game_board]

    return game_board, check_result, int(np.amax(game_board)), score, is_changed
