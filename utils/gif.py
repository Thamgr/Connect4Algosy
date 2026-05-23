from PIL import Image, ImageDraw
from enviroment.board import ROWS, COLS

CELL = 70
RADIUS = 28
BG = (30, 70, 200)
EMPTY = (240, 240, 240)
P1 = (230, 60, 60)
P2 = (240, 220, 60)


def save_gif(history, path, duration=500):
    frames = []
    for board in history:
        img = Image.new('RGB', (CELL * COLS, CELL * ROWS), BG)
        d = ImageDraw.Draw(img)
        for r in range(ROWS):
            for c in range(COLS):
                v = board.grid[r][c]
                color = EMPTY if v == 0 else (P1 if v == 1 else P2)
                cx = c * CELL + CELL // 2
                cy = (ROWS - 1 - r) * CELL + CELL // 2
                d.ellipse([cx - RADIUS, cy - RADIUS, cx + RADIUS, cy + RADIUS], fill=color)
        frames.append(img)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=duration, loop=0)
