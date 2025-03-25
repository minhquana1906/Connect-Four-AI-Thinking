import pygame
import numpy as np
from config import (
    BLUE,
    BLACK,
    RED,
    YELLOW,
    WHITE,
    GREEN,
    GRAY,
    SQUARESIZE,
    RADIUS,
    ROW_COUNT,
    COLUMN_COUNT,
    PLAYER_PIECE,
    AI_PIECE,
    WIDTH,
    HEIGHT,
    TITLE_FONT,
    MENU_FONT,
    INFO_FONT,
    MESSAGE_FONT,
    TIMER_FONT,
    NAME_FONT,
)


def draw_board(board, screen):
    """Draw the game board on the screen"""
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
    pygame.display.update()


def display_timer(screen, player_time, current_player):
    """Display the remaining time for current player"""
    minutes1 = int(player_time[0] // 60)
    seconds1 = int(player_time[0] % 60)
    minutes2 = int(player_time[1] // 60)
    seconds2 = int(player_time[1] % 60)

    # Display time for both players
    if current_player == 0:
        time1_color = RED
        time2_color = GRAY
    else:
        time1_color = GRAY
        time2_color = YELLOW

    time1_text = TIMER_FONT.render(f"{minutes1:02d}:{seconds1:02d}", 1, time1_color)
    time2_text = TIMER_FONT.render(f"{minutes2:02d}:{seconds2:02d}", 1, time2_color)

    # Position the timer under player names
    screen.blit(time1_text, (WIDTH // 4 - time1_text.get_width() // 2, 40))
    screen.blit(time2_text, (3 * WIDTH // 4 - time2_text.get_width() // 2, 40))


def draw_hover_piece(screen, posx, turn):
    """Draw the piece that follows the mouse cursor"""
    if turn == 0:  # Player 1's turn
        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
    else:  # Player 2's turn
        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
