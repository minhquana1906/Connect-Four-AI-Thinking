import pygame

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Game constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Player constants
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

# Calculate window dimensions
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# Initialize pygame fonts
pygame.font.init()
TITLE_FONT = pygame.font.SysFont("monospace", 50)
MENU_FONT = pygame.font.SysFont("monospace", 30)
INFO_FONT = pygame.font.SysFont("monospace", 20)
NAME_FONT = pygame.font.SysFont("monospace", 24)
INPUT_FONT = pygame.font.SysFont("monospace", 32)
MESSAGE_FONT = pygame.font.SysFont("monospace", 50)
TIMER_FONT = pygame.font.SysFont("monospace", 20)
