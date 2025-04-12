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
from ai import minimax
from ui.draw import draw_board, display_timer, draw_hover_piece, draw_pause_menu
from ui.input import get_difficulty
from config import (
    BLACK,
    RED,
    YELLOW,
    WHITE,
    SQUARESIZE,
    WIDTH,
    PLAYER,
    AI,
    PLAYER_PIECE,
    AI_PIECE,
)


class PlayerVsAIGame(Game):
    """Player vs AI game mode"""

    def __init__(self, screen):
        super().__init__(screen)
        # Get difficulty level (time limit)
        self.time_limit = get_difficulty(screen)

        # Player has time limit, AI has unlimited time
        self.default_time = [self.time_limit, float("inf")]
        self.player_time = [self.time_limit, float("inf")]
        self.last_time = pygame.time.get_ticks()

        # Player names
        self.player_name = "You"
        self.ai_name = "AI"

        # Random first turn
        import random

        self.turn = random.randint(PLAYER, AI)

        # Initial draw
        draw_board(self.board, self.screen)

    def run(self):
        """Main game loop"""
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            pause_action = None

            # Only update time if game is not paused
            if not self.paused:
                delta_time = (
                    current_time - self.last_time
                ) / 1000.0  # Convert to seconds

                # Update timer only for human player and when it's their turn
                if self.turn == PLAYER and not self.game_over:
                    self.player_time[PLAYER] -= delta_time

                    # Check for time out
                    if self.player_time[PLAYER] <= 0:
                        self.handle_timeout()

            self.last_time = current_time

            # Handle events
            for event in pygame.event.get():
                self.handle_quit_event(event)

                # Handle pause key - both pausing and unpausing
                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_p
                    and not self.game_over
                ):
                    pause_action = self.handle_pause_key(event)

                # Only process player inputs if not paused and it's player's turn
                elif not self.paused and self.turn == PLAYER:
                    self.handle_mouse_motion(event)
                    self.handle_player_move(event)

            # Process pause menu actions if any
            if pause_action == "restart":
                return "restart"
            elif pause_action == "menu":
                return "menu"

            # AI's turn - only process if not paused
            if self.turn == AI and not self.game_over and not self.paused:
                self.handle_ai_move()

            # Update UI at controlled frame rate
            if current_time - self.last_frame_time > 1000 / self.frame_rate:
                if not self.paused:  # Only update game UI if not paused
                    self.update_ui(current_time)
                self.last_frame_time = current_time

            self.handle_game_over()

        return None  # Default return when game ends normally

    def handle_timeout(self):
        """Handle player time running out"""
        self.player_time[PLAYER] = 0
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        label = self.message_font.render(f"{self.ai_name} wins on time!!", 1, YELLOW)
        self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
        self.game_over = True

    def handle_player_move(self, event):
        """Handle player move events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(self.board, col):
                row = get_next_open_row(self.board, col)
                drop_piece(self.board, row, col, PLAYER_PIECE)
                # Reset timer for player after making a move
                self.player_time[PLAYER] = self.default_time[PLAYER]

                if winning_move(self.board, PLAYER_PIECE):
                    self.display_winner(self.player_name, RED)
                else:
                    # Check for draw
                    self.check_draw()

                    # Switch turns if game not over
                    if not self.game_over:
                        self.turn = AI

                print_board(self.board)
                draw_board(self.board, self.screen)

    def handle_ai_move(self):
        """Handle AI move logic"""
        # AI makes a move using minimax
        col, minimax_score = minimax(self.board, 5, -math.inf, math.inf, True)

        if is_valid_location(self.board, col):
            # Add delay to make AI move visible
            pygame.time.wait(500)
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, AI_PIECE)

            if winning_move(self.board, AI_PIECE):
                self.display_winner(self.ai_name, YELLOW)
            else:
                # Check for draw
                self.check_draw()

                # Switch turns if game not over
                if not self.game_over:
                    self.turn = PLAYER

            print_board(self.board)
            draw_board(self.board, self.screen)

    def update_ui(self, current_time):
        """Update game UI elements"""
        # Clear top area
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

        # Display player names with active player highlighted
        if self.turn == PLAYER:
            p1_text = self.name_font.render(f"{self.player_name}", 1, RED)
            p2_text = self.name_font.render(f"{self.ai_name}", 1, (128, 128, 128))

            # Display turn indicator for player
            turn_text = self.name_font.render("'s turn", 1, WHITE)
            self.screen.blit(turn_text, (WIDTH // 4 + p1_text.get_width() // 2, 10))

            # Draw hover piece when it's player's turn
            draw_hover_piece(self.screen, self.mouse_pos_x, 0)
        else:
            p1_text = self.name_font.render(f"{self.player_name}", 1, (128, 128, 128))
            p2_text = self.name_font.render(f"{self.ai_name}", 1, YELLOW)

            # Display thinking text for AI
            thinking_text = self.name_font.render("thinking...", 1, WHITE)
            self.screen.blit(
                thinking_text, (3 * WIDTH // 4 + p2_text.get_width() // 2, 10)
            )

        self.screen.blit(p1_text, (WIDTH // 4 - p1_text.get_width() // 2, 10))
        self.screen.blit(p2_text, (3 * WIDTH // 4 - p2_text.get_width() // 2, 10))

        # Display timer (only for player)
        minutes = int(self.player_time[PLAYER] // 60)
        seconds = int(self.player_time[PLAYER] % 60)
        time_text = self.name_font.render(
            f"{minutes:02d}:{seconds:02d}",
            1,
            RED if self.turn == PLAYER else (128, 128, 128),
        )
        self.screen.blit(time_text, (WIDTH // 4 - time_text.get_width() // 2, 40))

        pygame.display.update()
        self.last_frame_time = current_time
