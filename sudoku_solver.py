import time
import copy

solvable = True


# False - wrong value
# True - correct value
def check_regions(array, i, j):
    square_x_start = (i // 3) * 3
    square_y_start = (j // 3) * 3

    for index in range(9):
        if (index != i and array[j][index] == array[j][i]) or (index != j and array[index][i] == array[j][i]):
            return False
    for y in range(square_y_start, square_y_start + 3):
        for x in range(square_x_start, square_x_start + 3):
            if (x, y) != (i, j) and array[y][x] == array[j][i]:
                return False
    return True


def list_fixed(board, fixed):
    for y in range(9):
        for x in range(9):
            if board[y][x] != 0:
                fixed[y][x] = True


# False - go back
# True - go forward
def solve_cell(board, x, y, fixed):
    if fixed[y][x]:
        return False

    for val in range(board[y][x] + 1, 10):
        board[y][x] = val
        if check_regions(board, x, y):
            return True

    board[y][x] = 0
    return False


def clear(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            board[y][x] = 0


def solve(board):
    """
    1) find empty
    2) try numbers until fits
    3) go to next
    4) if none fits, go back to previous
    """
    start = time.time()
    fixed = [[False] * 9 for _ in range(9)]
    list_fixed(board, fixed)
    y = 0
    x = 0
    while y < 9:
        while x < 9:
            if time.time() > start + 1:
                return False

            if board[y][x] == 0:
                while not solve_cell(board, x, y, fixed):
                    x -= 1
                    if x < 0:
                        y -= 1
                        x = 8
            x += 1
        y += 1
        x = 0
    return None


def copy_solved_cell(selected, board, board_new):
    board[selected[1]][selected[0]] = board_new[selected[1]][selected[0]]


def solve_board(board):
    board_new = copy.deepcopy(board)
    result = solve(board_new)

    if result is False:
        global solvable
        solvable = False
        return board

    return board_new


def solve_sudoku_region(selected, board, region):
    if selected is None:
        return

    board_new = solve_board(board)
    # row
    if region == 0:
        for val in range(9):
            selected_new = (val, selected[1])
            copy_solved_cell(selected_new, board, board_new)
    # column
    elif region == 1:
        for val in range(9):
            selected_new = (selected[0], val)
            copy_solved_cell(selected_new, board, board_new)

    # square
    elif region == 2:
        # beginning of current square
        x = selected[0] // 3 * 3
        y = selected[1] // 3 * 3
        for val_y in range(y, y + 3):
            for val_x in range(x, x + 3):
                selected_new = (val_x, val_y)
                copy_solved_cell(selected_new, board, board_new)
