from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

BLACK = (0, 0, 0)
WHITE = (1, 1, 1)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
CYAN = (0, 1, 1)
MAGENTA = (1, 0, 1)
YELLOW = (1, 1, 0)
ORANGE = (1, 0.647, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
INITIAL_POSITION = (GRID_WIDTH // 2, 0)
PIECES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]]
]

tetromino_color = random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE])
position = list(INITIAL_POSITION)
score = 0
start_time = time.time()

grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
tetromino = random.choice(PIECES)

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

def merge_tetromino(tetromino, position, grid):
    for y in range(len(tetromino)):
        for x in range(len(tetromino[y])):
            if tetromino[y][x] == 1:
                grid[position[1] + y][position[0] + x] = 1

def remove_completed_rows(grid):
    completed_rows = []
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            completed_rows.append(y)
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)
    return len(completed_rows)

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
    glutSwapBuffers()

def update(value):
    global position, tetromino, grid, score, start_time

    position[1] += 1
    if check_collision(tetromino, position, grid):
        position[1] -= 1
        merge_tetromino(tetromino, position, grid)
        completed_rows = remove_completed_rows(grid)
        score += completed_rows
        tetromino = random.choice(PIECES)
       
        position = list(INITIAL_POSITION)
        if check_collision(tetromino, position, grid):
            glutLeaveMainLoop()

    glutPostRedisplay()
    glutTimerFunc(500, update, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"Tetris")
    glutDisplayFunc(draw)
    glutTimerFunc(25, update, 0)
    glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
    glutMainLoop()

if __name__ == "__main__":
    main()
