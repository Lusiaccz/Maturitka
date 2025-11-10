import pygame
import random
import settings

# Initialize Pygame
pygame.init()


# Piece class
class Piece:
    def __init__(self):
        self.shape = random.choice(settings.SHAPES)
        self.color = random.choice(settings.COLORS)
        self.x = settings.COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid(self, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= settings.COLUMNS or ny >= settings.ROWS or (ny >= 0 and settings.grid[ny][nx]):
                        return False
        return True

    def place(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    settings.grid[self.y + y][self.x + x] = self.color

# Line clearing
def clear_lines():
    global grid
    settings.grid = [row for row in settings.grid if any(cell == 0 for cell in row)]
    while len(settings.grid) < settings.ROWS:
        settings.grid.insert(0, [0 for _ in range(settings.COLUMNS)])

# Drawing
def draw(win, piece):
    win.fill(settings.BLACK)
    for y in range(settings.ROWS):
        for x in range(settings.COLUMNS):
            color = settings.grid[y][x]
            if color:
                pygame.draw.rect(win, color, (x * settings.BLOCK_SIZE, y * settings.BLOCK_SIZE, settings.BLOCK_SIZE,
                                              settings.BLOCK_SIZE))
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(win, piece.color, ((piece.x + x) * settings.BLOCK_SIZE, (piece.y + y) * settings.BLOCK_SIZE,
                                                    settings.BLOCK_SIZE, settings.BLOCK_SIZE))
    pygame.display.update()

# Main loop
def main():
    win = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    piece = Piece()
    running = True
    FPS = settings.FPS

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
