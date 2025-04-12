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


def draw_pause_menu(screen):
    """Draw pause menu with continue, restart and main menu options"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
    screen.blit(overlay, (0, 0))

    # Title
    title = TITLE_FONT.render("GAME PAUSED", 1, WHITE)
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 4 - 40))

    # Create buttons
    button_width = 300
    button_height = 60
    button_x = WIDTH / 2 - button_width / 2

    # Continue button
    continue_button = pygame.Rect(
        button_x, HEIGHT / 2 - 30, button_width, button_height
    )
    pygame.draw.rect(screen, GREEN, continue_button)
    continue_text = MENU_FONT.render("Continue", 1, WHITE)
    screen.blit(
        continue_text, (WIDTH / 2 - continue_text.get_width() / 2, HEIGHT / 2 - 15)
    )

    # Restart button
    restart_button = pygame.Rect(button_x, HEIGHT / 2 + 60, button_width, button_height)
    pygame.draw.rect(screen, BLUE, restart_button)
    restart_text = MENU_FONT.render("Restart", 1, WHITE)
    screen.blit(
        restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2 + 75)
    )

    # Main menu button
    menu_button = pygame.Rect(button_x, HEIGHT / 2 + 150, button_width, button_height)
    pygame.draw.rect(screen, RED, menu_button)
    menu_text = MENU_FONT.render("Return to Main Menu", 1, WHITE)
    screen.blit(menu_text, (WIDTH / 2 - menu_text.get_width() / 2, HEIGHT / 2 + 165))

    # Hint text
    hint_text = INFO_FONT.render("Press 'P' again to continue", 1, WHITE)
    screen.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, HEIGHT * 3 / 4 + 50))

    pygame.display.update()

    return continue_button, restart_button, menu_button
