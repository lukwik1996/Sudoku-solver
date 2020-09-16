import pygame
import sys
import copy
import time
from sudoku import solve, clear


def exit_application():
    draw_text(position_text_info, 'Exit application? y/n', font_info, dark_grey)
    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_y or e.key == pygame.K_KP_ENTER or e.key == pygame.K_RETURN:
                    sys.exit()
                elif e.key == pygame.K_n:
                    return


def get_board_sizes(screen_width, screen_height):
    if screen_width > screen_height:
        board = screen_height
    else:
        board = screen_width

    cell = board / 9
    return cell, board


def get_cell_info(cell_width):
    coords = [[(0, 0) for _ in range(9)] for _ in range(9)]
    values = [[0 for _ in range(9)] for _ in range(9)]
    for y in range(9):
        for x in range(9):
            coords[y][x] = (cell_width * x + cell_width / 2, cell_width * y + cell_width / 2)
    return coords, values


def get_cell_by_mouse_coords(mouse_position, board_coords, cell_width):
    for y, row in enumerate(board_coords):
        for x, coord in enumerate(row):
            if coord[0] + cell_width / 2 > mouse_position[0] > coord[0] - cell_width / 2 and coord[1] - cell_width / 2 < mouse_position[1] < coord[1] + cell_width / 2:
                return x, y
    return None


def draw_board(cell_width, board_width):
    thick = 3
    thin = 2

    # 2 for loops so the thick lines are drawn on top of thin lines
    for i in range(0, 10):
        coord = i * cell_width
        line_width = thin
        color = dark_grey
        if i % 3 == 0:
            continue
        pygame.draw.line(screen, color, (coord, 0), (coord, board_width), line_width)
        pygame.draw.line(screen, color, (0, coord), (board_width, coord), line_width)

    for i in range(0, 10):
        coord = i * cell_width
        line_width = thick
        color = grey
        if i % 3 != 0:
            continue
        pygame.draw.line(screen, color, (coord, 0), (coord, board_width), line_width)
        pygame.draw.line(screen, color, (0, coord), (board_width, coord), line_width)


def fill_cell(value, coords):
    if value == 0:
        return
    draw_text(coords, str(value), font, white)


def fill_board(board, coords):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            fill_cell(board[y][x], coords[y][x])


def draw_button(coords, size, text, color, action=None):
    left = coords[0] - size[0] / 2
    top = coords[1] - size[1] / 2

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if left + size[0] > mouse[0] > left and top + size[1] > mouse[1] > top:
        if click[0] == 1 and action is not None:
            action()

    pygame.draw.rect(screen, color, ((left, top), size), 2)
    draw_text(coords, text, font_button, color)


def draw_text(coords, text, text_font, color):
    text = text_font.render(text, True, color)
    text_rect = text.get_rect(center=coords)
    screen.blit(text, text_rect)


def draw_board_buttons(board, coords, cell_width, board_width):
    screen.fill(black)
    draw_button(position_button_solve, button_size, 'Solve', white, action=solve_puzzle)
    draw_button(position_button_solve_cell, button_size, 'Solve current cell', white, action=solve_cell)
    draw_button(position_button_solve_square, button_size, 'Solve current square', white, action=solve_square)
    draw_button(position_button_solve_row, button_size, 'Solve current row', white, action=solve_row)
    draw_button(position_button_solve_column, button_size, 'Solve current column', white, action=solve_column)
    draw_button(position_button_clear, button_size, 'Clear puzzle', white, action=clear_puzzle)
    draw_button(position_button_load, button_big_size, 'Load puzzle from image', white)
    draw_text(position_button_load_info, '(not implemented yet)', font_button, grey)
    draw_board(cell_width, board_width)


def draw(board, coords, cell_width, board_width, selected=None):

    draw_board_buttons(board, coords, cell_width, board_width)
    if selected is not None:
        highlight_selected(coords[selected[1]][selected[0]], cell_width)

    global solvable
    if not solvable:
        draw_text(position_text_info, 'No solution found', font_info, dark_grey)

    fill_board(board, coords)
    pygame.display.update()

    if not solvable:
        solvable = True
        time.sleep(1)

        draw_board_buttons(board, coords, cell_width, board_width)
        fill_board(board, coords)
        pygame.display.update()


def solve_board(board):
    board_new = copy.deepcopy(board)
    result = solve(board_new)

    if result is False:
        global solvable
        solvable = False
        return board

    return board_new


def copy_solved_cell(selected, board, board_new):
    board[selected[1]][selected[0]] = board_new[selected[1]][selected[0]]


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


def solve_puzzle():
    global board_values
    board_new = solve_board(board_values)
    board_values = copy.deepcopy(board_new)


def solve_cell():
    board_new = solve_board(board_values)
    copy_solved_cell(selected_cell, board_values, board_new)


def clear_puzzle():
    clear(board_values)


def solve_row():
    solve_sudoku_region(selected_cell, board_values, 0)


def solve_column():
    solve_sudoku_region(selected_cell, board_values, 1)


def solve_square():
    solve_sudoku_region(selected_cell, board_values, 2)


def highlight_selected(coords, size):
    left = coords[0] - size / 2
    top = coords[1] - size / 2
    pygame.draw.rect(screen, highlight_frame_color, ((left, top), (size, size)), 2)


if __name__ == '__main__':

    pygame.init()
    pygame.font.init()

    button_size = (200, 30)
    button_big_size = (250, 30)
    position_button_solve = (1000, 50)
    position_button_solve_cell = (1000, 100)
    position_button_solve_square = (1000, 150)
    position_button_solve_row = (1000, 200)
    position_button_solve_column = (1000, 250)
    position_button_clear = (1000, 350)
    position_button_load = (1000, 550)
    position_button_load_info = (1000, 580)
    position_text_info = (1000, 680)

    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (200, 200, 200)
    dark_grey = (100, 100, 100)
    highlight_color = (200, 200, 100, 100)
    highlight_frame_color = (200, 200, 100)
    window_size = width, height = 1280, 720

    selected_cell = None
    solvable = True

    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption('Sudoku')
    img = pygame.image.load('icon.png')
    pygame.display.set_icon(img)
    font = pygame.font.SysFont('Arial', 50)
    font_info = pygame.font.SysFont('Arial', 30)
    font_button = pygame.font.SysFont('Arial', 20)

    cell_size, board_size = get_board_sizes(width, height)
    board_coords, board_values = get_cell_info(cell_size)

    while True:
        draw(board_values, board_coords, cell_size, board_size, selected_cell)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_application()
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                current_cell = get_cell_by_mouse_coords(pygame.mouse.get_pos(), board_coords, cell_size)

                # left mouse button
                if event.button == 1:
                    if current_cell is not None:
                        if selected_cell == current_cell:
                            selected_cell = None
                        else:
                            selected_cell = current_cell

                # right mouse button
                if event.button == 3:
                    board_values[current_cell[1]][current_cell[0]] = 0
                    draw(board_values, board_coords, cell_size, board_size)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_application()
                    continue

                if selected_cell is not None:
                    if event.key == pygame.K_1:
                        board_values[selected_cell[1]][selected_cell[0]] = 1
                    elif event.key == pygame.K_2:
                        board_values[selected_cell[1]][selected_cell[0]] = 2
                    elif event.key == pygame.K_3:
                        board_values[selected_cell[1]][selected_cell[0]] = 3
                    elif event.key == pygame.K_4:
                        board_values[selected_cell[1]][selected_cell[0]] = 4
                    elif event.key == pygame.K_5:
                        board_values[selected_cell[1]][selected_cell[0]] = 5
                    elif event.key == pygame.K_6:
                        board_values[selected_cell[1]][selected_cell[0]] = 6
                    elif event.key == pygame.K_7:
                        board_values[selected_cell[1]][selected_cell[0]] = 7
                    elif event.key == pygame.K_8:
                        board_values[selected_cell[1]][selected_cell[0]] = 8
                    elif event.key == pygame.K_9:
                        board_values[selected_cell[1]][selected_cell[0]] = 9
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        board_values[selected_cell[1]][selected_cell[0]] = 0
                    elif event.key == pygame.K_UP and selected_cell[1] > 0:
                        selected_cell = (selected_cell[0], selected_cell[1] - 1)
                    elif event.key == pygame.K_DOWN and selected_cell[1] < 8:
                        selected_cell = (selected_cell[0], selected_cell[1] + 1)
                    elif event.key == pygame.K_LEFT and selected_cell[0] > 0:
                        selected_cell = (selected_cell[0] - 1, selected_cell[1])
                    elif event.key == pygame.K_RIGHT and selected_cell[0] < 8:
                        selected_cell = (selected_cell[0] + 1, selected_cell[1])
