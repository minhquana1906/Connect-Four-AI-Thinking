import pygame
import sys
from config import SIZE
from ui.menu import draw_main_menu, show_about
from game.pvp import PlayerVsPlayerGame
from game.pvai import PlayerVsAIGame


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect 4")

    menu_active = True

    while menu_active:
        pvp_button, pvai_button, about_button, exit_button = draw_main_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if pvp_button.collidepoint(mouse_pos):
                    run_pvp_game(screen)

                elif pvai_button.collidepoint(mouse_pos):
                    run_pvai_game(screen)

                elif about_button.collidepoint(mouse_pos):
                    show_about(screen)

                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def run_pvp_game(screen):
    restart = True
    while restart:
        game = PlayerVsPlayerGame(screen)
        result = game.run()

        if result == "restart":
            restart = True
        elif result == "menu":
            return
        else:
            restart = False


def run_pvai_game(screen):
    restart = True
    while restart:
        game = PlayerVsAIGame(screen)
        result = game.run()

        if result == "restart":
            restart = True
        elif result == "menu":
            return
        else:
            restart = False


if __name__ == "__main__":
    main()
