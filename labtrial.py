# Import necessary libraries
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import keyboard

# Define color constants
BLACK = (0, 0, 0)
WHITE = (1, 1, 1)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
CYAN = (0, 1, 1)
MAGENTA = (1, 0, 1)
YELLOW = (1, 1, 0)
ORANGE = (1, 0.647, 0)

# Set screen dimensions and grid size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
INITIAL_POSITION = (GRID_WIDTH // 2, 0)

# Define Tetris pieces
PIECES = [
    [[1, 1, 1, 1]], # Line-shape (I)
    [[1, 1], [1, 1]], # Square-shape (O)
    [[1, 1, 0], [0, 1, 1]], # L-Shape (L)
    [[0, 1, 1], [1, 1, 0]], # J-Shape (J)
    [[1, 1, 1], [0, 1, 0]], # T-Shape (T)
    [[1, 1, 1], [0, 0, 1]], # S-Shape (S)
    [[1, 1, 1], [1, 0, 0]] # Z-Shape (Z)
]

# Select a random color for Tetrominos
tetromino_color = random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
position = list(INITIAL_POSITION)
score = 0
start_time = time.time()

# Initialize the grid and select a random Tetromino
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
tetromino = random.choice(PIECES)

# Initialize high score
high_score = 0

# Function to draw the grid lines
def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        glBegin(GL_LINES)
        glColor3fv(WHITE)
        glVertex2f(x, 0)
        glVertex2f(x, SCREEN_HEIGHT)
        glEnd()

    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        glBegin(GL_LINES)
        glColor3fv(WHITE)
        glVertex2f(0, y)
        glVertex2f(SCREEN_WIDTH, y)
        glEnd()

# Function to draw a Tetromino at a given position
def draw_tetromino(tetromino, position):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] == 1:
                glBegin(GL_QUADS)
                glColor3fv(tetromino_color)
                glVertex2f(position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE)
                glVertex2f(position[0] * GRID_SIZE + (x + 1) * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE)
                glVertex2f(position[0] * GRID_SIZE + (x + 1) * GRID_SIZE, position[1] * GRID_SIZE + (y + 1) * GRID_SIZE)
                glVertex2f(position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + (y + 1) * GRID_SIZE)
                glEnd()

# Function to check for collisions between Tetromino and the grid
def check_collision(tetromino, position, grid):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] == 1:
                if (
                    position[0] + x < 0
                    or position[0] + x >= GRID_WIDTH
                    or position[1] + y >= GRID_HEIGHT
                    or grid[position[1] + y][position[0] + x]
                ):
                    return True
    return False

# Function to merge a Tetromino into the grid
def merge_tetromino(tetromino, position, grid):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] == 1:
                grid[position[1] + y][position[0] + x] = 1

# Function to remove completed rows from the grid
def remove_completed_rows(grid):
    completed_rows = []
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            completed_rows.append(y)
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)
    return len(completed_rows)

# Function to update the score
def update_score(completed_rows):
    global score, high_score
    score += completed_rows
    if score > high_score:
        high_score = score

# Function to draw the score on the screen
def draw_score():
    glColor3fv(WHITE)
    glRasterPos2f(10, 10)
    score_str = f"Score: {score} High Score: {high_score}"
    for c in score_str:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))

# Function to draw the entire scenario
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_grid()
    draw_tetromino(tetromino, position)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                glBegin(GL_QUADS)
                glColor3fv(WHITE)
                glVertex2f(x * GRID_SIZE, y * GRID_SIZE)
                glVertex2f((x + 1) * GRID_SIZE, y * GRID_SIZE)
                glVertex2f((x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE)
                glVertex2f(x * GRID_SIZE, (y + 1) * GRID_SIZE)
                glEnd()
    draw_score()
    glutSwapBuffers()

paused = False # Variable to track whether the game is paused

# Function to handle keyboard input
def keyboard_callback(e):
    global position, tetromino, grid, score, start_time, paused

    if e.name == 'left':
        position[0] -= 1
        if check_collision(tetromino, position, grid):
            position[0] += 1

    elif e.name == 'right':
        position[0] += 1
        if check_collision(tetromino, position, grid):
            position[0] -= 1

    elif e.name == 'down':
        position[1] += 1
        if check_collision(tetromino, position, grid):
            position[1] -= 1
            merge_tetromino(tetromino, position, grid)
            completed_rows = remove_completed_rows(grid)
            update_score(completed_rows)
            tetromino = random.choice(PIECES)
            position = list(INITIAL_POSITION)
            if check_collision(tetromino, position, grid):
                glutLeaveMainLoop()

    elif e.name == 'up':  # Rotate the tetromino
        rotated_tetromino = list(zip(*reversed(tetromino)))
        if not check_collision(rotated_tetromino, position, grid):
            tetromino = rotated_tetromino

    

def update(value):
    global position, tetromino, grid, score, start_time, paused

    if not paused:
        position[1] += 1
        if check_collision(tetromino, position, grid):
            position[1] -= 1
            merge_tetromino(tetromino, position, grid)
            completed_rows = remove_completed_rows(grid)
            update_score(completed_rows)
            tetromino = random.choice(PIECES)
            position = list(INITIAL_POSITION)
            if check_collision(tetromino, position, grid):
                glutLeaveMainLoop()

        glutPostRedisplay()
        glutTimerFunc(500, update, 0)

# Function to reset the game
def reset_game():
    global grid, score, position, tetromino
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    score = 0
    position = list(INITIAL_POSITION)
    tetromino = random.choice(PIECES)

# Function to handle special key input
def keyboard_special_callback(key, x, y):
    global grid, score, position, tetromino, paused

    if key == GLUT_KEY_F1:  # New game
        reset_game()
    elif key == GLUT_KEY_F2:  # Pause/Resume the game
        paused = not paused
        if paused:
            glutTimerFunc(0, update, 0)  # Stop the timer
        else:
            glutTimerFunc(500, update, 0)  # Resume the timer


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"Tetris")
glutDisplayFunc(draw)
glutTimerFunc(25, update, 0)
glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
# Register the keyboard callback function
keyboard.hook(keyboard_callback)
# Register the special keys callback function
glutSpecialFunc(keyboard_special_callback)
glutMainLoop()


