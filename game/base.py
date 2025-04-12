import pygame
import sys
import math
import numpy as np
from board import (
    create_board,
    drop_piece,
    is_valid_location,
    get_next_open_row,
    print_board,
    winning_move,
    get_valid_locations,
)
from ui.draw import draw_board, display_timer, draw_hover_piece, draw_pause_menu
from config import BLACK, RED, YELLOW, WHITE, SQUARESIZE, WIDTH, MESSAGE_FONT, NAME_FONT


class Game:
    """Base game class with common functionality"""

    def __init__(self, screen):
        self.screen = screen
        self.board = create_board()
        self.game_over = False
        self.paused = False
        self.message_font = (
            pygame.font.SysFont("monospace", 50)
            if not pygame.font.get_init()
            else MESSAGE_FONT
        )
        self.name_font = (
            pygame.font.SysFont("monospace", 24)
            if not pygame.font.get_init()
            else NAME_FONT
        )

        # Track frame rate to avoid flickering
        self.last_frame_time = 0
        self.frame_rate = 30
        self.mouse_pos_x = WIDTH // 2

    def handle_quit_event(self, event):
        """Handle quit event"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def handle_mouse_motion(self, event):
        """Track mouse position"""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos_x = event.pos[0]

    def handle_pause_key(self, event):
        """Handle pause key (P) press"""
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_p
            and not self.game_over
        ):
            if not self.paused:
                # Pausing the game
                self.paused = True
                return self.handle_pause_menu()
            else:
                # Unpausing the game (should redraw the board)
                self.paused = False
                draw_board(self.board, self.screen)
                return "continue"
        return None

    def handle_pause_menu(self):
        """Display pause menu and handle option selection"""
        continue_button, restart_button, menu_button = draw_pause_menu(self.screen)

        pause_menu_active = True
        while pause_menu_active and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check for P key to unpause directly
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.paused = False
                    pause_menu_active = False
                    # Redraw the board to clear the pause menu
                    draw_board(self.board, self.screen)
                    return "continue"

                # Check for button clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Continue button clicked
                    if continue_button.collidepoint(mouse_pos):
                        self.paused = False
                        pause_menu_active = False
                        # Redraw the board to clear the pause menu
                        draw_board(self.board, self.screen)
                        return "continue"

                    # Restart button clicked
                    elif restart_button.collidepoint(mouse_pos):
                        self.paused = False
                        return "restart"

                    # Main menu button clicked
                    elif menu_button.collidepoint(mouse_pos):
                        self.paused = False
                        self.game_over = True
                        return "menu"

            pygame.display.update()

    def handle_game_over(self):
        """Wait when game is over"""
        if self.game_over:
            pygame.time.wait(3000)

    def check_draw(self):
        """Check for a draw condition"""
        if not self.game_over and len(get_valid_locations(self.board)) == 0:
            pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            label = self.message_font.render("It's a draw!", 1, WHITE)
            self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
            self.game_over = True

    def display_winner(self, winner_name, winner_color):
        """Display winner message"""
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        label = self.message_font.render(f"{winner_name} wins!!", 1, winner_color)
        self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
        self.game_over = True
