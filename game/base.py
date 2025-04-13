import pygame
import sys
from board import create_board, get_valid_locations, print_board, winning_move
from ui.draw import draw_board, draw_pause_menu
from config import BLACK, WHITE, SQUARESIZE, WIDTH, MESSAGE_FONT, NAME_FONT


class Game:
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

        self.last_frame_time = 0
        self.frame_rate = 30
        self.mouse_pos_x = WIDTH // 2

    def handle_quit_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def handle_mouse_motion(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos_x = event.pos[0]

    def handle_pause_key(self, event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
            and not self.game_over
        ):
            if not self.paused:
                self.paused = True
                return self.handle_pause_menu()
            else:
                self.paused = False
                draw_board(self.board, self.screen)
                return "continue"
        return None

    def handle_pause_menu(self):
        continue_button, restart_button, menu_button = draw_pause_menu(self.screen)

        pause_menu_active = True
        while pause_menu_active and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = False
                    pause_menu_active = False
                    draw_board(self.board, self.screen)
                    return "continue"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if continue_button.collidepoint(mouse_pos):
                        self.paused = False
                        pause_menu_active = False
                        draw_board(self.board, self.screen)
                        return "continue"

                    elif restart_button.collidepoint(mouse_pos):
                        self.paused = False
                        return "restart"

                    elif menu_button.collidepoint(mouse_pos):
                        self.paused = False
                        self.game_over = True
                        return "menu"

            pygame.display.update()

    def handle_game_over(self):
        if self.game_over:
            pygame.time.wait(3000)

    def check_draw(self):
        if not self.game_over and len(get_valid_locations(self.board)) == 0:
            pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            label = self.message_font.render("It's a draw!", 1, WHITE)
            self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
            pygame.display.update()
            self.game_over = True
            return True
        return False

    def display_winner(self, winner_name, winner_color):
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        label = self.message_font.render(f"{winner_name} wins!!", 1, winner_color)
        self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
        self.game_over = True
        pygame.display.update()

    def handle_move_completion(self, piece_type, player_name, color):
        """Common logic to execute after a move is made"""
        print_board(self.board)
        draw_board(self.board, self.screen)

        if winning_move(self.board, piece_type):
            self.display_winner(player_name, color)
            return True

        if self.check_draw():
            return True

        return False
