import pygame
import math
import random
from game.base import Game
from board import (
    drop_piece,
    is_valid_location,
    get_next_open_row,
    print_board,
    winning_move,
)
from ai import minimax
from ui.draw import draw_board, draw_hover_piece
from ui.input import get_difficulty
from config import (
    BLACK,
    RED,
    YELLOW,
    WHITE,
    GRAY,
    RADIUS,
    SQUARESIZE,
    WIDTH,
    PLAYER,
    AI,
    PLAYER_PIECE,
    AI_PIECE,
)


class PlayerVsAIGame(Game):

    def __init__(self, screen):
        super().__init__(screen)
        self.time_limit = get_difficulty(screen)

        self.default_time = [self.time_limit, float("inf")]
        self.player_time = [self.time_limit, float("inf")]
        self.last_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.player_name = "Player"
        self.ai_name = "AI"

        self.turn = random.randint(PLAYER, AI)

        draw_board(self.board, self.screen)

    def run(self):
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            pause_action = None

            if not self.paused:
                delta_time = (current_time - self.last_time) / 1000.0

                if self.turn == PLAYER and not self.game_over:
                    self.player_time[PLAYER] -= delta_time
                    if self.player_time[PLAYER] <= 0:
                        self.handle_timeout()

                self.last_time = current_time

            for event in pygame.event.get():
                self.handle_quit_event(event)

                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                    and not self.game_over
                ):
                    pause_action = self.handle_pause_key(event)
                    if pause_action == "restart":
                        return "restart"
                    elif pause_action == "menu":
                        return "menu"

                elif not self.paused and self.turn == PLAYER:
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE * 2)
                        )
                        posx = event.pos[0]
                        self.mouse_pos_x = posx
                        pygame.draw.circle(
                            self.screen, RED, (posx, int(SQUARESIZE * 1.5)), RADIUS
                        )

                        if self.turn == PLAYER:
                            p1_text = self.name_font.render(
                                f"{self.player_name}", 1, RED
                            )
                            p2_text = self.name_font.render(f"{self.ai_name}", 1, GRAY)
                            turn_text = self.name_font.render("'s turn", 1, WHITE)
                            self.screen.blit(
                                p1_text, (WIDTH // 4 - p1_text.get_width() // 2, 10)
                            )
                            self.screen.blit(
                                p2_text, (3 * WIDTH // 4 - p2_text.get_width() // 2, 10)
                            )
                            self.screen.blit(
                                turn_text, (WIDTH // 4 + p1_text.get_width() // 2, 10)
                            )

                            minutes = int(self.player_time[PLAYER] // 60)
                            seconds = int(self.player_time[PLAYER] % 60)
                            time_text = self.name_font.render(
                                f"{minutes:02d}:{seconds:02d}",
                                1,
                                RED if self.turn == PLAYER else GRAY,
                            )
                            self.screen.blit(
                                time_text, (WIDTH // 4 - time_text.get_width() // 2, 40)
                            )

                        pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE * 2)
                        )
                        self.handle_player_move(event)

                        if not self.game_over:
                            self.update_ui(current_time)

            if self.turn == AI and not self.game_over and not self.paused:
                self.handle_ai_move()

            if current_time - self.last_frame_time > 1000 / self.frame_rate:
                if not self.paused:
                    self.update_ui(current_time)
                self.last_frame_time = current_time

            if self.handle_game_over():
                pygame.display.update()
                return None

            pygame.display.update()
            self.clock.tick(60)

        return None

    def handle_timeout(self):
        self.player_time[PLAYER] = 0
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        label = self.message_font.render(f"{self.ai_name} wins on time!!", 1, YELLOW)
        self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
        self.game_over = True
        pygame.display.update()

    def handle_player_move(self, event):
        posx = event.pos[0]
        col = int(math.floor(posx / SQUARESIZE))

        if is_valid_location(self.board, col):
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, PLAYER_PIECE)
            self.player_time[PLAYER] = self.default_time[PLAYER]

            game_ended = self.handle_move_completion(
                PLAYER_PIECE, self.player_name, RED
            )

            if not self.game_over and not game_ended:
                self.turn = AI

    def handle_ai_move(self):
        col, minimax_score = minimax(self.board, 5, -math.inf, math.inf, True)

        if is_valid_location(self.board, col):
            pygame.time.wait(500)
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, AI_PIECE)

            game_ended = self.handle_move_completion(AI_PIECE, self.ai_name, YELLOW)

            if not self.game_over and not game_ended:
                self.turn = PLAYER

    def update_ui(self, current_time):
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE * 2))

        if self.turn == PLAYER:
            p1_text = self.name_font.render(f"{self.player_name}", 1, RED)
            p2_text = self.name_font.render(f"{self.ai_name}", 1, (128, 128, 128))

            turn_text = self.name_font.render("'s turn", 1, WHITE)
            self.screen.blit(turn_text, (WIDTH // 4 + p1_text.get_width() // 2, 10))

            draw_hover_piece(self.screen, self.mouse_pos_x, 0)
        else:
            p1_text = self.name_font.render(f"{self.player_name}", 1, (128, 128, 128))
            p2_text = self.name_font.render(f"{self.ai_name}", 1, YELLOW)

            thinking_text = self.name_font.render(" thinking...", 1, WHITE)
            self.screen.blit(
                thinking_text, (3 * WIDTH // 4 + p2_text.get_width() // 2, 10)
            )

        self.screen.blit(p1_text, (WIDTH // 4 - p1_text.get_width() // 2, 10))
        self.screen.blit(p2_text, (3 * WIDTH // 4 - p2_text.get_width() // 2, 10))

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
