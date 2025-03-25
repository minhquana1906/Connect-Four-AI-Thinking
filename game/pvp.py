import pygame
import math
from game.base import Game
from board import (
    create_board,
    drop_piece,
    is_valid_location,
    get_next_open_row,
    print_board,
    winning_move,
)
from ui.draw import draw_board, display_timer, draw_hover_piece
from ui.input import get_player_names
from config import BLACK, RED, YELLOW, WHITE, SQUARESIZE, WIDTH, PLAYER_PIECE, AI_PIECE


class PlayerVsPlayerGame(Game):
    """Player vs Player game mode"""

    def __init__(self, screen):
        super().__init__(screen)
        # Get player names
        self.player1_name, self.player2_name = get_player_names(screen)

        # Set time limit for PvP mode (120 seconds per player)
        self.time_limit = 120
        self.player_time = [self.time_limit, self.time_limit]
        self.last_time = pygame.time.get_ticks()

        # Start with player 1
        self.turn = 0

        # Initial draw
        draw_board(self.board, self.screen)

    def run(self):
        """Main game loop"""
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - self.last_time) / 1000.0  # Convert to seconds

            # Update timer
            if not self.game_over:
                self.player_time[self.turn] -= delta_time

                # Check for time out
                if self.player_time[self.turn] <= 0:
                    self.handle_timeout()

            self.last_time = current_time

            # Handle events
            for event in pygame.event.get():
                self.handle_quit_event(event)
                self.handle_mouse_motion(event)
                self.handle_player_move(event)

            # Update UI at controlled frame rate
            if current_time - self.last_frame_time > 1000 / self.frame_rate:
                self.update_ui(current_time)

            self.handle_game_over()

    def handle_timeout(self):
        """Handle player time running out"""
        self.player_time[self.turn] = 0
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        winner = self.player2_name if self.turn == 0 else self.player1_name
        winner_color = YELLOW if self.turn == 0 else RED
        self.display_winner(winner, winner_color)

    def handle_player_move(self, event):
        """Handle player move events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(self.board, col):
                row = get_next_open_row(self.board, col)

                if self.turn == 0:
                    drop_piece(self.board, row, col, PLAYER_PIECE)
                    if winning_move(self.board, PLAYER_PIECE):
                        self.display_winner(self.player1_name, RED)
                else:
                    drop_piece(self.board, row, col, AI_PIECE)
                    if winning_move(self.board, AI_PIECE):
                        self.display_winner(self.player2_name, YELLOW)

                print_board(self.board)
                draw_board(self.board, self.screen)

                # Check for draw
                self.check_draw()

                # Switch turns if game not over
                if not self.game_over:
                    self.turn += 1
                    self.turn = self.turn % 2

    def update_ui(self, current_time):
        """Update game UI elements"""
        # Clear top area
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

        # Display player names with active player highlighted
        if self.turn == 0:
            p1_text = self.name_font.render(f"{self.player1_name}", 1, RED)
            p2_text = self.name_font.render(f"{self.player2_name}", 1, (128, 128, 128))
        else:
            p1_text = self.name_font.render(f"{self.player1_name}", 1, (128, 128, 128))
            p2_text = self.name_font.render(f"{self.player2_name}", 1, YELLOW)

        self.screen.blit(p1_text, (WIDTH // 4 - p1_text.get_width() // 2, 10))
        self.screen.blit(p2_text, (3 * WIDTH // 4 - p2_text.get_width() // 2, 10))

        # Display timer
        display_timer(self.screen, self.player_time, self.turn)

        # Display turn indicator
        turn_text = self.name_font.render("'s turn", 1, WHITE)
        if self.turn == 0:
            self.screen.blit(turn_text, (WIDTH // 4 + p1_text.get_width() // 2, 10))
        else:
            self.screen.blit(turn_text, (3 * WIDTH // 4 + p2_text.get_width() // 2, 10))

        # Draw hover piece
        draw_hover_piece(self.screen, self.mouse_pos_x, self.turn)

        pygame.display.update()
        self.last_frame_time = current_time
