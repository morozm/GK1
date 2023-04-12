import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
ORANGE = (255,127,80)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 900, 900
pygame.display.set_caption("3D Cube")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scale = 50
angle = 0
distanceX = 0
distanceY = 0
distanceZ = 5
moveX = 0
moveY = 0
moveZ = 0
number_of_figures = 4
center = [WIDTH/2, HEIGHT/2]

figures = [[] for i in range(number_of_figures)]
figures[0].append(np.matrix([ 1,     1,      1]))
figures[0].append(np.matrix([ 3,     1,      1]))
figures[0].append(np.matrix([ 3,     3,      1]))
figures[0].append(np.matrix([ 1,     3,      1]))
figures[0].append(np.matrix([ 1,     1,     -1]))
figures[0].append(np.matrix([ 3,     1,     -1]))
figures[0].append(np.matrix([ 3,     3,     -1]))
figures[0].append(np.matrix([ 1,     3,     -1]))

figures[1].append(np.matrix([-3,     1,      1]))
figures[1].append(np.matrix([-1,     1,      1]))
figures[1].append(np.matrix([-1,     3,      1]))
figures[1].append(np.matrix([-3,     3,      1]))
figures[1].append(np.matrix([-3,     1,     -1]))
figures[1].append(np.matrix([-1,     1,     -1]))
figures[1].append(np.matrix([-1,     3,     -1]))
figures[1].append(np.matrix([-3,     3,     -1]))

figures[2].append(np.matrix([-3,    -3,      1]))
figures[2].append(np.matrix([-1,    -3,      1]))
figures[2].append(np.matrix([-1,    -1,      1]))
figures[2].append(np.matrix([-3,    -1,      1]))
figures[2].append(np.matrix([-3,    -3,     -1]))
figures[2].append(np.matrix([-1,    -3,     -1]))
figures[2].append(np.matrix([-1,    -1,     -1]))
figures[2].append(np.matrix([-3,    -1,     -1]))

figures[3].append(np.matrix([ 1,    -3,      1]))
figures[3].append(np.matrix([ 3,    -3,      1]))
figures[3].append(np.matrix([ 3,    -1,      1]))
figures[3].append(np.matrix([ 1,    -1,      1]))
figures[3].append(np.matrix([ 1,    -3,     -1]))
figures[3].append(np.matrix([ 3,    -3,     -1]))
figures[3].append(np.matrix([ 3,    -1,     -1]))
figures[3].append(np.matrix([ 1,    -1,     -1]))
    
projection_matrix = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, float(1/distanceZ), 1],
])

for i in range(number_of_figures):
    projected_points = [[
        [n, n] for n in range(len(figures[i]))
    ]for j in range(number_of_figures)]

def connect_points(figure, i, j):
    pygame.draw.line(
        screen, WHITE, (projected_points[figure][i][0], projected_points[figure][i][1]), (projected_points[figure][j][0], projected_points[figure][j][1]))

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    screen.fill(BLACK)

    translation = np.matrix([
        [1,             0,              0,              moveX],
        [0,             1,              0,              moveY],
        [0,             0,              1,              moveZ],
        [0,             0,              0,              1],
    ])

    rotation_z = np.matrix([
        [cos(angle),    -sin(angle),    0,              0],
        [sin(angle),    cos(angle),     0,              0],
        [0,             0,              1,              0],
        [0,             0,              0,              1],
    ])

    rotation_y = np.matrix([
        [cos(angle),    0,              sin(angle),     0],
        [0,             1,              0,              0],
        [-sin(angle),   0,              cos(angle),     0],
        [0,             0,              0,              1],
    ])

    rotation_x = np.matrix([
        [1,             0,              0,              0],
        [0,             cos(angle),     -sin(angle),    0],
        [0,             sin(angle),     cos(angle),     0],
        [0,             0,              0,              1],
    ])
    angle += 0.01
    moveX += 0.01

    i = 0
    fig = 0
    for figure in figures:
        for point in figure:
            point = point.reshape(3, 1)
            point=np.r_[point, np.matrix([1])]

            rotated2d = point
            # rotated2d = np.dot(rotation_z, rotated2d)
            rotated2d = np.dot(rotation_y, rotated2d)
            # rotated2d /= rotated2d[3][0]
            # rotated2d = np.dot(rotation_x, rotated2d)

            translated = rotated2d
            # translated = np.dot(translation, translated)

            projected2d = translated
            projected2d[0][0]=projected2d[0][0]*distanceZ/(projected2d[2][0]+distanceZ)
            projected2d[1][0]=projected2d[1][0]*distanceZ/(projected2d[2][0]+distanceZ)
            projected2d[2][0]=0
            x=int(projected2d[0][0] * scale + center[0])
            y=int(projected2d[1][0] * scale + center[1])
            projected_points[fig][i] = [x, y]
            pygame.draw.circle(screen, ORANGE, (x,y), 5)
            i+=1
        i = 0
        fig+=1

    connect_points(0, 0, 1)
    connect_points(0, 1, 2)
    connect_points(0, 2, 3)
    connect_points(0, 3, 0)
    connect_points(0, 4, 5)
    connect_points(0, 5, 6)
    connect_points(0, 6, 7)
    connect_points(0, 7, 4)
    connect_points(0, 0, 4)
    connect_points(0, 1, 5)
    connect_points(0, 2, 6)
    connect_points(0, 3, 7)

    connect_points(1, 0, 1)
    connect_points(1, 1, 2)
    connect_points(1, 2, 3)
    connect_points(1, 3, 0)
    connect_points(1, 4, 5)
    connect_points(1, 5, 6)
    connect_points(1, 6, 7)
    connect_points(1, 7, 4)
    connect_points(1, 0, 4)
    connect_points(1, 1, 5)
    connect_points(1, 2, 6)
    connect_points(1, 3, 7)

    connect_points(2, 0, 1)
    connect_points(2, 1, 2)
    connect_points(2, 2, 3)
    connect_points(2, 3, 0)
    connect_points(2, 4, 5)
    connect_points(2, 5, 6)
    connect_points(2, 6, 7)
    connect_points(2, 7, 4)
    connect_points(2, 0, 4)
    connect_points(2, 1, 5)
    connect_points(2, 2, 6)
    connect_points(2, 3, 7)

    connect_points(3, 0, 1)
    connect_points(3, 1, 2)
    connect_points(3, 2, 3)
    connect_points(3, 3, 0)
    connect_points(3, 4, 5)
    connect_points(3, 5, 6)
    connect_points(3, 6, 7)
    connect_points(3, 7, 4)
    connect_points(3, 0, 4)
    connect_points(3, 1, 5)
    connect_points(3, 2, 6)
    connect_points(3, 3, 7)

    pygame.display.update()