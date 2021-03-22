import pygame
import sys
import copy
import time
from sudoku_solver import clear, copy_solved_cell, solve_board, solve_sudoku_region
import config


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


def fill_cell(value, coords):
    if value == 0:
        return
    draw_text(coords, str(value), font, white)


def fill_board(board, coords):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            fill_cell(board[y][x], coords[y][x])


def draw_board(cell_width, board_width):
    thick = 3
    thin = 2

    # 2 for loops so the thick lines are drawn on top of thin lines
    for i in range(0, 10):
        coord = int(i * cell_width)
        board_width = int(board_width)
        line_width = thin

        color = dark_grey
        if i % 3 == 0:
            continue
        pygame.draw.line(screen, color, (coord, 0), (coord, board_width), line_width)
        pygame.draw.line(screen, color, (0, coord), (board_width, coord), line_width)

    for i in range(0, 10):
        coord = int(i * cell_width)
        line_width = thick
        color = grey
        if i % 3 != 0:
            continue
        pygame.draw.line(screen, color, (coord, 0), (coord, board_width), line_width)
        pygame.draw.line(screen, color, (0, coord), (board_width, coord), line_width)


def draw_button(coords, size, text, color, action=None):
    left = int(coords[0] - size[0] / 2)
    top = int(coords[1] - size[1] / 2)

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


def draw_board_buttons(cell_width, board_width):
    screen.fill(black)
    draw_button(position_button_solve, button_size, 'Solve', white, action=solve_puzzle)
    draw_button(position_button_solve_cell, button_size, 'Solve current cell', white, action=solve_cell)
    draw_button(position_button_solve_square, button_size, 'Solve current square', white, action=solve_square)
    draw_button(position_button_solve_row, button_size, 'Solve current row', white, action=solve_row)
    draw_button(position_button_solve_column, button_size, 'Solve current column', white, action=solve_column)
    draw_button(position_button_clear, button_size, 'Clear puzzle', white, action=clear_puzzle)

    # TODO implement loading sudoku board from image
    # draw_button(position_button_load, button_big_size, 'Load puzzle from image', white, action=)
    # draw_text(position_button_load_info, '(not implemented yet)', font_button, grey)
    draw_board(cell_width, board_width)


def draw(board, coords, cell_width, board_width, selected=None):

    draw_board_buttons(cell_width, board_width)
    if selected is not None:
        highlight_selected(coords[selected[1]][selected[0]], cell_width)

    if not config.solvable:
        draw_text(position_text_info, 'No solution found', font_info, dark_grey)

    fill_board(board, coords)
    pygame.display.update()

    if not config.solvable:
        config.solvable = True
        time.sleep(1)

        draw_board_buttons(cell_width, board_width)
        fill_board(board, coords)
        pygame.display.update()


def highlight_selected(coords, size):
    left = int(coords[0] - size / 2)
    top = int(coords[1] - size / 2)
    size = int(size)
    pygame.draw.rect(screen, highlight_frame_color, ((left, top), (size, size)), 2)


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


if __name__ == '__main__':

    pygame.init()
    pygame.font.init()

    # position and size values
    window_size = width, height = 1280, 720

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

    # color values
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (200, 200, 200)
    dark_grey = (100, 100, 100)
    highlight_color = (200, 200, 100, 100)
    highlight_frame_color = (200, 200, 100)

    selected_cell = None

    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption('Sudoku')
    img = pygame.image.load('icon.png')
    pygame.display.set_icon(img)

    # fonts
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
                    # number keys
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        board_values[selected_cell[1]][selected_cell[0]] = 1
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        board_values[selected_cell[1]][selected_cell[0]] = 2
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        board_values[selected_cell[1]][selected_cell[0]] = 3
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        board_values[selected_cell[1]][selected_cell[0]] = 4
                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        board_values[selected_cell[1]][selected_cell[0]] = 5
                    elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        board_values[selected_cell[1]][selected_cell[0]] = 6
                    elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        board_values[selected_cell[1]][selected_cell[0]] = 7
                    elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        board_values[selected_cell[1]][selected_cell[0]] = 8
                    elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        board_values[selected_cell[1]][selected_cell[0]] = 9

                    # clearing cell value
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        board_values[selected_cell[1]][selected_cell[0]] = 0

                    # moving around the board with arrow keys
                    elif event.key == pygame.K_UP and selected_cell[1] > 0:
                        selected_cell = (selected_cell[0], selected_cell[1] - 1)
                    elif event.key == pygame.K_DOWN and selected_cell[1] < 8:
                        selected_cell = (selected_cell[0], selected_cell[1] + 1)
                    elif event.key == pygame.K_LEFT and selected_cell[0] > 0:
                        selected_cell = (selected_cell[0] - 1, selected_cell[1])
                    elif event.key == pygame.K_RIGHT and selected_cell[0] < 8:
                        selected_cell = (selected_cell[0] + 1, selected_cell[1])
