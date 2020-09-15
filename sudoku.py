import time


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


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - -')

        for j in range(len(board[i])):
            if j % 3 == 0 and j != 0:
                print('| ', end='')

            if j == len(board[0]) - 1:
                print(board[i][j])
            else:
                print(board[i][j], end=' ')

# for testing purposes
def main():
    fixed_cells = [[False] * 9 for _ in range(9)]
    sudoku_board = [
        [0, 1, 0, 0, 0, 0, 0, 8, 0],
        [0, 5, 7, 0, 0, 0, 4, 0, 0],
        [0, 8, 0, 7, 0, 2, 0, 0, 0],
        [0, 7, 0, 0, 4, 0, 0, 9, 0],
        [4, 0, 0, 6, 7, 0, 8, 0, 5],
        [5, 0, 0, 0, 9, 8, 0, 3, 0],
        [8, 3, 2, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 8],
        [1, 9, 0, 0, 0, 4, 5, 0, 0]
    ]

    print_board(sudoku_board)

    solve(sudoku_board)

    print('\n----------------\n')
    print_board(sudoku_board)


if __name__ == '__main__':
    main()
