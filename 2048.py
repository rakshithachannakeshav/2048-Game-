import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SIZE = 4
TILE_SIZE = 180
GAP_SIZE = 5
WINDOW_SIZE = SIZE * TILE_SIZE + (SIZE + 1) * GAP_SIZE
FONT_SIZE = 40
BACKGROUND_COLOR = (0,0,0)
TILE_COLORS = {
    0: (255,255,255),
    2: (238, 228, 218),
    4: (128,128,128),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
FONT_COLOR = (0,0,0)

# Initialize the game window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("2048")

# Load the font
font = pygame.font.Font(None, FONT_SIZE)

def draw_board(board):
    """Draws the game board on the Pygame window."""
    screen.fill(BACKGROUND_COLOR)
    for i in range(SIZE):
        for j in range(SIZE):
            value = board[i][j]
            color = TILE_COLORS.get(value, (60, 58, 50))
            rect = pygame.Rect(j * (TILE_SIZE + GAP_SIZE) + GAP_SIZE,
                               i * (TILE_SIZE + GAP_SIZE) + GAP_SIZE,
                               TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            if value != 0:
                # Render text and center it within the tile
                text = font.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    pygame.display.update()

def add_new_tile(board):
    """Adds a new tile (2 or 4) to a random empty cell in the board."""
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def rotate_board_clockwise(board):
    """Rotates the board 90 degrees clockwise."""
    return [list(row) for row in zip(*board[::-1])]

def rotate_board_counterclockwise(board):
    """Rotates the board 90 degrees counterclockwise."""
    return rotate_board_clockwise(rotate_board_clockwise(rotate_board_clockwise(board)))

def merge_row_left(row):
    """Merges tiles in a row to the left and returns the new row."""
    non_zero_row = [num for num in row if num != 0]
    new_row = []
    skip = False
    for i in range(len(non_zero_row)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zero_row) and non_zero_row[i] == non_zero_row[i + 1]:
            new_row.append(non_zero_row[i] * 2)
            skip = True
        else:
            new_row.append(non_zero_row[i])
    return new_row + [0] * (SIZE - len(new_row))

def move_left(board):
    """Moves the board left by merging tiles in each row."""
    new_board = []
    for row in board:
        new_board.append(merge_row_left(row))
    return new_board

def move_right(board):
    """Moves the board right by merging tiles in each row."""
    new_board = []
    for row in board:
        new_board.append(list(reversed(merge_row_left(list(reversed(row))))))
    return new_board

def move_up(board):
    """Moves the board up by rotating counterclockwise and merging tiles."""
    rotated_board = rotate_board_counterclockwise(board)
    new_board = move_left(rotated_board)
    return rotate_board_clockwise(new_board)

def move_down(board):
    """Moves the board down by rotating clockwise and merging tiles."""
    rotated_board = rotate_board_clockwise(board)
    new_board = move_left(rotated_board)
    return rotate_board_counterclockwise(new_board)

def is_game_over(board):
    """Checks if the game is over by verifying if no more moves can be made."""
    for row in board:
        for i in range(SIZE - 1):
            if row[i] == row[i + 1] or row[i] == 0:
                return False
    for col in range(SIZE):
        for i in range(SIZE - 1):
            if board[i][col] == board[i + 1][col]:
                return False
    return True

def main():
    """Main function to run the 2048 game."""
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    draw_board(board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    board = move_right(board)
                elif event.key == pygame.K_UP:
                    board = move_up(board)
                elif event.key == pygame.K_DOWN:
                    board = move_down(board)
                else:
                    continue

                add_new_tile(board)
                draw_board(board)

                if is_game_over(board):
                    print("Game Over!")
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()