import pygame
import sys
from config import WIDTH, HEIGHT, SIZE
from ui.menu import draw_main_menu, show_about
from game.pvp import PlayerVsPlayerGame
from game.pvai import PlayerVsAIGame


def main():
    """Main entry point for the Connect 4 game"""
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect 4")

    menu_active = True

    while menu_active:
        # Display main menu and get button references
        pvp_button, pvai_button, about_button, exit_button = draw_main_menu(screen)

        # Handle menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # PvP button clicked
                if pvp_button.collidepoint(mouse_pos):
                    game = PlayerVsPlayerGame(screen)
                    game.run()
                    # Return to menu after game ends

                # PvAI button clicked
                elif pvai_button.collidepoint(mouse_pos):
                    game = PlayerVsAIGame(screen)
                    game.run()
                    # Return to menu after game ends

                # About button clicked
                elif about_button.collidepoint(mouse_pos):
                    show_about(screen)

                # Exit button clicked
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
