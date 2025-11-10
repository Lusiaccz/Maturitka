import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
FPS = 5

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [(0, 255, 255), (255, 165, 0), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128)]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Game grid
grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

# Piece class
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid(self, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= COLUMNS or ny >= ROWS or (ny >= 0 and grid[ny][nx]):
                        return False
        return True

    def place(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color

# Line clearing
def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < ROWS:
        grid.insert(0, [0 for _ in range(COLUMNS)])

# Drawing
def draw(win, piece):
    win.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLUMNS):
            color = grid[y][x]
            if color:
                pygame.draw.rect(win, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(win, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.update()

# Main loop
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    piece = Piece()
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and piece.valid(dx=-1):
                    piece.x -= 1
                elif event.key == pygame.K_RIGHT and piece.valid(dx=1):
                    piece.x += 1
                elif event.key == pygame.K_DOWN and piece.valid(dy=1):
                    piece.y += 1
                elif event.key == pygame.K_UP:
                    piece.rotate()
                    if not piece.valid():
                        piece.rotate()
                        piece.rotate()
                        piece.rotate()

        if piece.valid(dy=1):
            piece.y += 1
        else:
            piece.place()
            clear_lines()
            piece = Piece()
            if not piece.valid():
                running = False

        draw(win, piece)

    pygame.quit()

if __name__ == "__main__":
    main()
