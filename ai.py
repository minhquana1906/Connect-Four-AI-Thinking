import math
import random
from config import PLAYER_PIECE, AI_PIECE, EMPTY, WINDOW_LENGTH, COLUMN_COUNT, ROW_COUNT
from board import (
    drop_piece,
    get_next_open_row,
    winning_move,
    get_valid_locations,
    is_terminal_node,
)


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board, PLAYER_PIECE, AI_PIECE)

    if depth == 0 or is_terminal:
        return get_terminal_score(board, is_terminal)

    if maximizingPlayer:
        return maximize_score(board, depth, alpha, beta, valid_locations)
    else:
        return minimize_score(board, depth, alpha, beta, valid_locations)


def get_terminal_score(board, is_terminal):
    if is_terminal:
        if winning_move(board, AI_PIECE):
            return (None, 100000000000000)
        elif winning_move(board, PLAYER_PIECE):
            return (None, -10000000000000)
        else:
            return (None, 0)
    else:
        return (None, score_position(board, AI_PIECE))


def maximize_score(board, depth, alpha, beta, valid_locations):
    value = -math.inf
    column = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        drop_piece(b_copy, row, col, AI_PIECE)
        new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]

        if new_score > value:
            value = new_score
            column = col

        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return column, value


def minimize_score(board, depth, alpha, beta, valid_locations):
    value = math.inf
    column = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        drop_piece(b_copy, row, col, PLAYER_PIECE)
        new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]

        if new_score < value:
            value = new_score
            column = col

        beta = min(beta, value)
        if alpha >= beta:
            break

    return column, value


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col
