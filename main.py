import os
import sys
import pygame
import math
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_position = [2.0, 5.0, 2.0, 1.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

def draw_ground(sz):
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glNormal3f(0, 1, 0)
    vertices = (
        (-sz, -1, -sz),
        (-sz, -1, sz),
        (sz, -1, sz),
        (sz, -1, -sz)
    )

    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()

def draw_ball(position, radius, color):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3f(color[0], color[1], color[2])
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    gluDeleteQuadric(quadric)
    glPopMatrix()
def calc_cur_radius(ball_position, ground_size):
    x = ball_position[0]
    z = ball_position[2]
    distance_from_center = math.sqrt(x ** 2 + z ** 2)
    max_distance = ground_size * 0.7
    normalized_distance = min(distance_from_center / max_distance, 1.0)
    size = 3.0 - normalized_distance * 1.0
    return max(size, 0.1)

def calc_cur_color(ball_position, bound_sz, current_time):
    x = ball_position[0]
    z = ball_position[2]
    r = 0.5 + 0.5 * (x + bound_sz) / (2 * bound_sz)
    g = 0.5 + 0.5 * (z + bound_sz) / (2 * bound_sz)
    b = 0.5 + 0.5 * math.sin(current_time * 2)
    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return [r, g, b]

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -50)
    glEnable(GL_NORMALIZE)
    glEnable(GL_DEPTH_TEST)
    init_lighting()

    bound_sz = 20.0
    speed = 5.0
    ball_radius = 40.0
    ball_position = [0, 0, 0]
    ball_speed = [0.05*speed, 0*speed, 0.03*speed]
    bounds = [-bound_sz, bound_sz, -bound_sz, bound_sz]

    start_time = time.time()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cur_time = time.time() - start_time

        ball_position[0] += ball_speed[0]
        ball_position[2] += ball_speed[2]

        if ball_position[0] < bounds[0] or ball_position[0] > bounds[1]:
            ball_speed[0] = -ball_speed[0]
        if ball_position[2] < bounds[2] or ball_position[2] > bounds[3]:
            ball_speed[2] = -ball_speed[2]

        size_var = 0.2 * math.sin(cur_time * 2)
        current_radius = ball_radius + size_var
        cur_radius = calc_cur_radius(ball_position, bound_sz)
        cur_color = calc_cur_color(ball_position, bound_sz, cur_time)
        ball_position[1] = cur_radius - 1

        glPushMatrix()

        #glRotatef(30, 1, 0, 0)
        #glRotatef(cur_time * 5 * speed, 0, 1, 0)

        glRotatef(90, bound_sz/2, 0, 0)
        
        draw_ground(bound_sz + 5.0)
        draw_ball(ball_position, cur_radius, cur_color)

        glPopMatrix()

        pygame.display.flip()
        clock.tick(60) 
    
if __name__ == "__main__":
    main()


# if sys.path[0] in ("", os.getcwd()):
#     sys.path.pop(0)

# if __package__ == "":
#     path = os.path.dirname(os.path.dirname(__file__))
#     sys.path.insert(0, path)

# if __name__ == "__main__":
#     main()
