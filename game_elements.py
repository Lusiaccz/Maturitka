import pygame
import random
import settings

class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base_color = settings.WHITE

    def draw(self, win):
        mouse = pygame.mouse.get_pos()
        color = (180, 180, 180) if self.rect.collidepoint(mouse) else self.base_color
        pygame.draw.rect(win, (40, 40, 40), self.rect, border_radius=8)
        pygame.draw.rect(win, color, self.rect, 2, border_radius=8)
        text_surf = self.font.render(self.text, True, settings.WHITE)
        win.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

class Piece:
    def __init__(self, grid, shape_index):
        self.grid = grid
        self.shape_index = shape_index
        self.shape = settings.SHAPES[self.shape_index]
        self.color = settings.COLORS[self.shape_index % len(settings.COLORS)]
        self.x = settings.COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        old_shape = self.shape
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        if not self.valid(): self.shape = old_shape

    def valid(self, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= settings.COLUMNS or ny >= settings.ROWS: return False
                    if ny >= 0 and self.grid[ny][nx]: return False
        return True

    def place(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell: self.grid[self.y + y][self.x + x] = self.color