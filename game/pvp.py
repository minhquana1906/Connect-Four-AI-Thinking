import pygame
import math
from game.base import Game
from board import (
    drop_piece,
    is_valid_location,
    get_next_open_row,
    print_board,
    winning_move,
)
from ui.draw import draw_board
from ui.input import get_player_names
from config import (
    BLACK,
    RED,
    YELLOW,
    WHITE,
    GRAY,
    SQUARESIZE,
    WIDTH,
    PLAYER_PIECE,
    AI_PIECE,
    RADIUS,
)


class PlayerVsPlayerGame(Game):

    def __init__(self, screen):
        super().__init__(screen)
        self.player1_name, self.player2_name = get_player_names(screen)

        self.time_limit = 120
        self.default_time = [self.time_limit, self.time_limit]
        self.player_time = [self.time_limit, self.time_limit]
        self.last_time = pygame.time.get_ticks()

        self.turn = 0

        self.clock = pygame.time.Clock()
        draw_board(self.board, self.screen)

    def run(self):
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            pause_action = None

            if not self.paused:
                delta_time = (current_time - self.last_time) / 1000.0

                if not self.game_over:
                    self.player_time[self.turn] -= delta_time

                    if self.player_time[self.turn] <= 0:
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

                    if self.paused or pause_action == "continue":
                        self.last_time = pygame.time.get_ticks()

                elif not self.paused:
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE * 2)
                        )
                        posx = event.pos[0]
                        self.mouse_pos_x = posx

                        self.draw_ui_info()

                        player_color = RED if self.turn == 0 else YELLOW
                        pygame.draw.circle(
                            self.screen,
                            player_color,
                            (posx, int(SQUARESIZE * 1.5)),
                            RADIUS,
                        )

                        pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE * 2)
                        )
                        self.handle_player_move(event)

            if pause_action == "restart":
                return "restart"
            elif pause_action == "menu":
                return "menu"

            if current_time - self.last_frame_time > 1000 / self.frame_rate:
                if not self.paused:
                    self.update_ui(current_time)
                self.last_frame_time = current_time

            if self.handle_game_over():
                return None
            pygame.display.update()
            self.clock.tick(60)

        return None

    def draw_ui_info(self):
        if self.turn == 0:
            p1_color = RED
            p2_color = GRAY
            p1_text = self.name_font.render(f"{self.player1_name}", 1, p1_color)
            p2_text = self.name_font.render(f"{self.player2_name}", 1, p2_color)
            turn_text = self.name_font.render("'s turn", 1, WHITE)
            self.screen.blit(turn_text, (WIDTH // 4 + p1_text.get_width() // 2, 10))
        else:
            p1_color = GRAY
            p2_color = YELLOW
            p1_text = self.name_font.render(f"{self.player1_name}", 1, p1_color)
            p2_text = self.name_font.render(f"{self.player2_name}", 1, p2_color)
            turn_text = self.name_font.render("'s turn", 1, WHITE)
            self.screen.blit(turn_text, (3 * WIDTH // 4 + p2_text.get_width() // 2, 10))

        self.screen.blit(p1_text, (WIDTH // 4 - p1_text.get_width() // 2, 10))
        self.screen.blit(p2_text, (3 * WIDTH // 4 - p2_text.get_width() // 2, 10))

        minutes1 = int(self.player_time[0] // 60)
        seconds1 = int(self.player_time[0] % 60)
        minutes2 = int(self.player_time[1] // 60)
        seconds2 = int(self.player_time[1] % 60)

        time1_text = self.name_font.render(
            f"{minutes1:02d}:{seconds1:02d}", 1, p1_color
        )
        time2_text = self.name_font.render(
            f"{minutes2:02d}:{seconds2:02d}", 1, p2_color
        )

        self.screen.blit(time1_text, (WIDTH // 4 - time1_text.get_width() // 2, 40))
        self.screen.blit(time2_text, (3 * WIDTH // 4 - time2_text.get_width() // 2, 40))

    def handle_timeout(self):
        self.player_time[self.turn] = 0
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE * 2))
        winner = self.player2_name if self.turn == 0 else self.player1_name
        winner_color = YELLOW if self.turn == 0 else RED
        self.display_winner(winner, winner_color)

    def handle_player_move(self, event):
        posx = event.pos[0]
        col = int(math.floor(posx / SQUARESIZE))

        if is_valid_location(self.board, col):
            row = get_next_open_row(self.board, col)

            if self.turn == 0:
                drop_piece(self.board, row, col, PLAYER_PIECE)
                self.player_time[self.turn] = self.default_time[self.turn]
                game_ended = self.handle_move_completion(
                    PLAYER_PIECE, self.player1_name, RED
                )
            else:
                drop_piece(self.board, row, col, AI_PIECE)
                self.player_time[self.turn] = self.default_time[self.turn]
                game_ended = self.handle_move_completion(
                    AI_PIECE, self.player2_name, YELLOW
                )

            if not self.game_over and not game_ended:
                self.turn = (self.turn + 1) % 2

    def update_ui(self, current_time):
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE * 2))

        self.draw_ui_info()

        player_color = RED if self.turn == 0 else YELLOW
        pygame.draw.circle(
            self.screen, player_color, (self.mouse_pos_x, int(SQUARESIZE * 1.5)), RADIUS
        )

        pygame.display.update()
        self.last_frame_time = current_time
