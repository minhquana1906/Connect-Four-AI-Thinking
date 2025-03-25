import pygame
import sys
from config import (
    BLACK,
    WHITE,
    BLUE,
    GREEN,
    RED,
    YELLOW,
    WIDTH,
    HEIGHT,
    TITLE_FONT,
    MENU_FONT,
    INFO_FONT,
)


def draw_main_menu(screen):
    """Draw the main menu with all options"""
    screen.fill(BLACK)
    title = TITLE_FONT.render("Connect 4", 1, WHITE)
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 50))

    # Create buttons
    pvp_button = pygame.Rect(WIDTH / 2 - 150, 150, 300, 80)
    pvai_button = pygame.Rect(WIDTH / 2 - 150, 250, 300, 80)
    about_button = pygame.Rect(WIDTH / 2 - 150, 350, 300, 80)
    quit_button = pygame.Rect(WIDTH / 2 - 150, 450, 300, 80)

    pygame.draw.rect(screen, BLUE, pvp_button)
    pygame.draw.rect(screen, BLUE, pvai_button)
    pygame.draw.rect(screen, GREEN, about_button)
    pygame.draw.rect(screen, RED, quit_button)

    # Add text to buttons
    pvp_text = MENU_FONT.render("Player vs Player", 1, WHITE)
    pvai_text = MENU_FONT.render("Player vs AI", 1, WHITE)
    about_text = MENU_FONT.render("About", 1, WHITE)
    quit_text = MENU_FONT.render("Quit", 1, WHITE)

    screen.blit(pvp_text, (WIDTH / 2 - pvp_text.get_width() / 2, 175))
    screen.blit(pvai_text, (WIDTH / 2 - pvai_text.get_width() / 2, 275))
    screen.blit(about_text, (WIDTH / 2 - about_text.get_width() / 2, 375))
    screen.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, 475))

    pygame.display.update()
    return pvp_button, pvai_button, about_button, quit_button


def show_about(screen):
    """Display information about the game"""
    screen.fill(BLACK)
    title = TITLE_FONT.render("About Connect 4", 1, WHITE)
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 50))

    # Read rules from rules.txt file
    try:
        with open("rules.txt", "r", encoding="utf-8") as file:
            info_lines = file.read().splitlines()
    except FileNotFoundError:
        # Fallback to default text if file isn't found
        info_lines = [
            "Connect 4 is a two-player connection game where players",
            "take turns dropping colored discs into a grid.",
            "",
            "The objective is to be the first to form a horizontal,",
            "vertical, or diagonal line of four discs.",
            "",
            "Game modes:",
            "- Player vs Player: Play against another person",
            "- Player vs AI: Play against the computer",
            "",
            "Created by: Team 02",
            "Version: 1.0",
            "",
            "(Could not load rules.txt file)",
        ]

    # Display the rules text
    y_pos = 120
    for line in info_lines:
        text = INFO_FONT.render(line, 1, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, y_pos))
        y_pos += 30

    # Back button
    back_button = pygame.Rect(WIDTH / 2 - 100, 600, 200, 50)
    pygame.draw.rect(screen, BLUE, back_button)
    back_text = INFO_FONT.render("Back to Menu", 1, WHITE)
    screen.blit(back_text, (WIDTH / 2 - back_text.get_width() / 2, 615))

    pygame.display.update()

    # Wait for user to go back
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
