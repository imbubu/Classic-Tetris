import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Define shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Create the grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Function to draw the grid
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Function to check for collisions
def check_collision(shape, offset):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid_x = x + offset[0]
                grid_y = y + offset[1]
                if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT or (grid_y >= 0 and grid[grid_y][grid_x] != 0):
                    return True
    return False

# Function to merge the shape into the grid
def merge_shape(shape, offset, color):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid_y = y + offset[1]
                grid_x = x + offset[0]
                if grid_y >= 0:
                    grid[grid_y][grid_x] = color

# Function to clear completed lines
def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = GRID_HEIGHT - len(new_grid)
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(lines_cleared)] + new_grid
    grid = new_grid

# Function to draw the current shape
def draw_shape(shape, offset, color):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, ((x + offset[0]) * BLOCK_SIZE, (y + offset[1]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to rotate the shape
def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

# Main game loop
def main():
    global grid
    clock = pygame.time.Clock()
    current_shape = random.choice(SHAPES)
    shape_color = random.choice([RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE])
    shape_offset = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]

    fall_time = 0
    fall_speed = 500  # milliseconds

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_shape(current_shape, shape_offset, shape_color)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_offset = [shape_offset[0] - 1, shape_offset[1]]
                    if not check_collision(current_shape, new_offset):
                        shape_offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = [shape_offset[0] + 1, shape_offset[1]]
                    if not check_collision(current_shape, new_offset):
                        shape_offset = new_offset
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate(current_shape)
                    if not check_collision(rotated_shape, shape_offset):
                        current_shape = rotated_shape

        # Falling shape logic
        fall_time += clock.get_time()
        if fall_time >= fall_speed:
            fall_time = 0
            new_offset = [shape_offset[0], shape_offset[1] + 1]
            if not check_collision(current_shape, new_offset):
                shape_offset = new_offset
            else:
                merge_shape(current_shape, shape_offset, shape_color)
                clear_lines()
                current_shape = random.choice(SHAPES)
                shape_color = random.choice([RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE])
                shape_offset = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                if check_collision(current_shape, shape_offset):
                    print("Game Over")
                    running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()