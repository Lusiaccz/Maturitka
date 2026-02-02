import pygame
WIDTH, HEIGHT = 300, 600
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [(0, 255, 255), (255, 165, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128)]
WHITE = (255, 255, 255)
COLUMNS = 10
ROWS = 20
FPS = 5
MENU_MAIN = "main"
MENU_SETTINGS = "settings"
LEVEL_UP_SCORE = 1000
MAX_FPS = 30
RESOLUTIONS = [(300, 600), (360, 720), (450, 900), (600, 1200)]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
