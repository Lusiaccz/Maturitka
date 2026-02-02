import pygame
import random
import settings
from database import init_db, save_score
from game_elements import Button, Piece

# Inicializace Pygame
pygame.init()


# =====================
# POMOCNÉ FUNKCE
# =====================
def draw_text_center(win, text, font, color, x, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    win.blit(surf, rect)


def get_next_shape_index(bag):
    if not bag:
        bag.extend(range(len(settings.SHAPES)))
        random.shuffle(bag)
    return bag.pop()


# =====================
# HERNÍ OBRAZOVKY
# =====================
def get_name_screen(win, bg_image):
    font = pygame.font.SysFont("arial", 32)
    name, run = "", True
    while run:
        win.blit(bg_image, (0, 0))
        draw_text_center(win, "Zadej jméno a ENTER:", font, settings.WHITE, settings.WIDTH // 2,
                         settings.HEIGHT // 2 - 50)

        name_surf = font.render(name + "|", True, (255, 255, 0))
        name_rect = name_surf.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 10))
        win.blit(name_surf, name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    run = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10 and (event.unicode.isalnum() or event.unicode == " "):
                        name += event.unicode
        pygame.display.update()
    return name


def game_over_menu(win, score):
    title_font = pygame.font.SysFont("arial", 48, bold=True)
    button_font = pygame.font.SysFont("arial", 28)
    cx, cy = settings.WIDTH // 2, settings.HEIGHT // 2

    overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, 0))

    replay_btn = Button(cx - 90, cy + 20, 180, 50, "REPLAY", button_font)
    menu_btn = Button(cx - 90, cy + 90, 180, 50, "MENU", button_font)

    draw_text_center(win, "GAME OVER", title_font, (255, 50, 50), cx, cy - 100)
    draw_text_center(win, f"Score: {score}", button_font, settings.WHITE, cx, cy - 40)

    while True:
        replay_btn.draw(win)
        menu_btn.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if replay_btn.clicked(event): return "RESTART"
            if menu_btn.clicked(event): return "MENU"
        pygame.display.update()


def menu(win, bg_original):
    title_font = pygame.font.SysFont("arial", 50, bold=True)
    button_font = pygame.font.SysFont("arial", 28)
    label_font = pygame.font.SysFont("arial", 20, bold=True)  # Font pro popisky
    state, res_index = settings.MENU_MAIN, 0
    bg_image = pygame.transform.scale(bg_original, (settings.WIDTH, settings.HEIGHT))

    while True:
        win.blit(bg_image, (0, 0))
        cx, cy = settings.WIDTH // 2, settings.HEIGHT // 2

        if state == settings.MENU_MAIN:
            btns = [Button(cx - 90, cy - 60, 180, 50, "PLAY", button_font),
                    Button(cx - 90, cy + 10, 180, 50, "SETTINGS", button_font),
                    Button(cx - 90, cy + 80, 180, 50, "QUIT", button_font)]
            draw_text_center(win, "TETRIS", title_font, settings.WHITE, cx, cy - 150)
            for b in btns: b.draw(win)
        else:
            btns = [Button(cx - 110, cy, 40, 40, "-", button_font),
                    Button(cx + 70, cy, 40, 40, "+", button_font),
                    Button(cx - 90, cy + 80, 180, 50, "BACK", button_font)]

            draw_text_center(win, "SETTINGS", title_font, settings.WHITE, cx, cy - 150)
            # Nápis RESOLUTION nad výběrem
            draw_text_center(win, "RESOLUTION", label_font, (settings.WHITE), cx, cy - 40)
            draw_text_center(win, f"{settings.WIDTH}x{settings.HEIGHT}", button_font, settings.WHITE, cx, cy + 20)
            for b in btns: b.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False, None
            if state == settings.MENU_MAIN:
                if btns[0].clicked(event): return True, bg_image
                if btns[1].clicked(event): state = settings.MENU_SETTINGS
                if btns[2].clicked(event): return False, None
            else:
                if btns[2].clicked(event): state = settings.MENU_MAIN
                if btns[0].clicked(event) or btns[1].clicked(event):
                    res_index = (res_index + (1 if btns[1].clicked(event) else -1)) % len(settings.RESOLUTIONS)
                    settings.WIDTH, settings.HEIGHT = settings.RESOLUTIONS[res_index]
                    settings.BLOCK_SIZE = settings.HEIGHT // settings.ROWS
                    win = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
                    bg_image = pygame.transform.scale(bg_original, (settings.WIDTH, settings.HEIGHT))
        pygame.display.update()


# =====================
# VYKRESLOVÁNÍ HRY
# =====================
def draw_game(win, grid, piece, score, level, bg_image, player_name):
    win.blit(bg_image, (0, 0))
    for y in range(settings.ROWS):
        for x in range(settings.COLUMNS):
            if grid[y][x]:
                pygame.draw.rect(win, grid[y][x],
                                 (x * settings.BLOCK_SIZE, y * settings.BLOCK_SIZE, settings.BLOCK_SIZE,
                                  settings.BLOCK_SIZE))
            pygame.draw.rect(win, (155, 161, 157),
                             (x * settings.BLOCK_SIZE, y * settings.BLOCK_SIZE, settings.BLOCK_SIZE,
                              settings.BLOCK_SIZE), 1)

    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(win, piece.color,
                                 ((piece.x + x) * settings.BLOCK_SIZE, (piece.y + y) * settings.BLOCK_SIZE,
                                  settings.BLOCK_SIZE, settings.BLOCK_SIZE))

    font = pygame.font.SysFont("arial", 20, bold=True)
    draw_text_center(win, f"{player_name} | S: {score} | L: {level}", font, settings.WHITE, settings.WIDTH // 2, 20)
    pygame.display.update()


# =====================
# HLAVNÍ FUNKCE
# =====================
def main():
    init_db()
    win = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Tetris Arcade")

    try:
        bg_original = pygame.image.load("background.png").convert()
    except:
        bg_original = pygame.Surface((1200, 1200))
        bg_original.fill((20, 20, 20))

    while True:
        run_game, bg_image = menu(win, bg_original)
        if not run_game: break

        player_name = get_name_screen(win, bg_image)
        if not player_name: continue

        playing = True
        while playing:
            grid = [[0 for _ in range(settings.COLUMNS)] for _ in range(settings.ROWS)]
            score, level, fall_time, bag = 0, 1, 0, []
            piece = Piece(grid, get_next_shape_index(bag))
            clock = pygame.time.Clock()
            game_active = True

            while game_active:
                fall_speed = 1000 // min(settings.MAX_FPS, settings.FPS + level)
                fall_time += clock.get_rawtime()
                clock.tick()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and piece.valid(dx=-1): piece.x -= 1
                        if event.key == pygame.K_RIGHT and piece.valid(dx=1): piece.x += 1
                        if event.key == pygame.K_DOWN and piece.valid(dy=1): piece.y += 1
                        if event.key == pygame.K_UP: piece.rotate()

                if fall_time >= fall_speed:
                    if piece.valid(dy=1):
                        piece.y += 1
                    else:
                        piece.place()
                        # Mazání řádků a skóre
                        full_rows = [r for r in grid if all(c != 0 for c in r)]
                        lines_cleared = len(full_rows)
                        if lines_cleared > 0:
                            grid[:] = [[0] * settings.COLUMNS for _ in range(lines_cleared)] + [r for r in grid if
                                                                                                any(c == 0 for c in r)]
                            score += {1: 100, 2: 300, 3: 500, 4: 800}.get(lines_cleared, 0)
                            level = score // settings.LEVEL_UP_SCORE + 1

                        piece = Piece(grid, get_next_shape_index(bag))
                        if not piece.valid():
                            save_score(player_name, score, level)
                            action = game_over_menu(win, score)
                            if action == "RESTART":
                                game_active = False
                            elif action == "MENU":
                                game_active = False
                                playing = False
                            else:
                                pygame.quit();
                                return
                    fall_time = 0

                draw_game(win, grid, piece, score, level, bg_image, player_name)

    pygame.quit()


if __name__ == "__main__":
    main()