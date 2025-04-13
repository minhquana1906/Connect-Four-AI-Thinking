import pygame
import sys
from config import (
    BLACK,
    WHITE,
    RED,
    YELLOW,
    GREEN,
    WIDTH,
    INPUT_FONT,
    INFO_FONT,
    EASY,
    MEDIUM,
    HARD,
)


def get_player_names(screen):
    screen.fill(BLACK)
    title = INPUT_FONT.render("Enter Player Names", 1, WHITE)
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 50))

    player1_text = INFO_FONT.render("Player 1:", 1, RED)
    player2_text = INFO_FONT.render("Player 2:", 1, YELLOW)

    screen.blit(player1_text, (WIDTH / 2 - 220, 150))
    screen.blit(player2_text, (WIDTH / 2 - 220, 250))

    player1_box = pygame.Rect(WIDTH / 2 - 40, 145, 300, 40)
    player2_box = pygame.Rect(WIDTH / 2 - 40, 245, 300, 40)

    pygame.draw.rect(screen, WHITE, player1_box, 2)
    pygame.draw.rect(screen, WHITE, player2_box, 2)

    continue_button = pygame.Rect(WIDTH / 2 - 100, 350, 200, 50)
    pygame.draw.rect(screen, GREEN, continue_button)
    continue_text = INFO_FONT.render("Continue", 1, WHITE)
    screen.blit(continue_text, (WIDTH / 2 - continue_text.get_width() / 2, 365))

    player1_name = "Player 1"
    player2_name = "Player 2"
    active_input = None

    name1_surface = INPUT_FONT.render(player1_name, 1, WHITE)
    name2_surface = INPUT_FONT.render(player2_name, 1, WHITE)
    screen.blit(name1_surface, (player1_box.x + 10, player1_box.y + 5))
    screen.blit(name2_surface, (player2_box.x + 10, player2_box.y + 5))

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player1_box.collidepoint(event.pos):
                    active_input = "player1"
                elif player2_box.collidepoint(event.pos):
                    active_input = "player2"
                elif continue_button.collidepoint(event.pos):
                    return player1_name, player2_name
                else:
                    active_input = None

            if event.type == pygame.KEYDOWN:
                if active_input == "player1":
                    if event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_input = "player2"
                    elif len(player1_name) < 15:
                        player1_name += event.unicode
                elif active_input == "player2":
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        return player1_name, player2_name
                    elif len(player2_name) < 15:
                        player2_name += event.unicode

        pygame.draw.rect(
            screen,
            BLACK,
            (
                player1_box.x + 2,
                player1_box.y + 2,
                player1_box.width - 4,
                player1_box.height - 4,
            ),
        )
        pygame.draw.rect(
            screen,
            BLACK,
            (
                player2_box.x + 2,
                player2_box.y + 2,
                player2_box.width - 4,
                player2_box.height - 4,
            ),
        )

        if active_input == "player1":
            pygame.draw.rect(screen, RED, player1_box, 2)
            pygame.draw.rect(screen, WHITE, player2_box, 2)
        elif active_input == "player2":
            pygame.draw.rect(screen, WHITE, player1_box, 2)
            pygame.draw.rect(screen, YELLOW, player2_box, 2)
        else:
            pygame.draw.rect(screen, WHITE, player1_box, 2)
            pygame.draw.rect(screen, WHITE, player2_box, 2)

        name1_surface = INPUT_FONT.render(player1_name, 1, WHITE)
        name2_surface = INPUT_FONT.render(player2_name, 1, WHITE)
        screen.blit(name1_surface, (player1_box.x + 10, player1_box.y + 5))
        screen.blit(name2_surface, (player2_box.x + 10, player2_box.y + 5))

        pygame.display.update()


def get_difficulty(screen):
    difficulties = {
        "Easy": EASY,
        "Medium": MEDIUM,
        "Hard": HARD,
    }

    screen.fill(BLACK)
    title = INPUT_FONT.render("Select Difficulty", 1, WHITE)
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 50))

    button_height = 70
    button_width = 300
    button_x = WIDTH / 2 - button_width / 2

    buttons = {}
    y_pos = 250

    for diff in difficulties:
        buttons[diff] = pygame.Rect(button_x, y_pos, button_width, button_height)
        pygame.draw.rect(screen, GREEN, buttons[diff])

        diff_text = INPUT_FONT.render(diff, 1, WHITE)
        screen.blit(
            diff_text,
            (
                WIDTH / 2 - diff_text.get_width() / 2,
                y_pos + button_height / 2 - diff_text.get_height() / 2,
            ),
        )

        y_pos += button_height + 20

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for diff, button in buttons.items():
                    if button.collidepoint(event.pos):
                        return difficulties[diff]

    return difficulties["Medium"]
