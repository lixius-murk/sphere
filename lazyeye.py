import pygame
import math
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from colorsystem import ColorSystem
from bltype import blType

def set_background_color(blindness_type):
    if blindness_type == blType.Achromatopsia:
        glClearColor(0.9, 0.9, 0.9, 1.0)  # Светло-серый для ч.б.
    else:
        glClearColor(0.2, 0.2, 0.3, 1.0)  # Темно-синий

def init_lighting(): 
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_position = [0.0, 50.0, 0.0, 1.0]  # Прямо сверху
    light_ambient = [0.4, 0.4, 0.4, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [0.5, 0.5, 0.5, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

def draw_ground(sz, blindness_type):
    if blindness_type == blType.Achromatopsia:
        glColor3f(0.7, 0.7, 0.7)  # Серый для ч.б.
    else:
        glColor3f(0.2, 0.4, 0.2)  # Зеленый
    
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-sz, 0, -sz)
    glVertex3f(-sz, 0, sz)
    glVertex3f(sz, 0, sz)
    glVertex3f(sz, 0, -sz)
    glEnd()


def draw_ball(position, radius, color):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3f(color[0], color[1], color[2])
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def calc_cur_color(bl: blType, ball_position, ground_size, current_time):
    cs = ColorSystem()
    variations = 8
    x_norm = (ball_position[0] + ground_size) / (2 * ground_size)
    z_norm = (ball_position[2] + ground_size) / (2 * ground_size)
    
    if bl == blType.Healthy:
        color_type = 'primary'
    elif bl == blType.Deuteranopia:
        color_type = 'secondary'  
    elif bl == blType.Protanopia:
        color_type = 'accent'    
    elif bl == blType.Tritanopia:
        color_type = 'primary'
    else:  # Achromatopsia
        color_type = 'primary'
    
    base_color = cs.get_base_color(bl, color_type)
    lab_colors = cs.generate_colors(base_color, variations, x_norm, z_norm, current_time)
    
    color_index = int((x_norm + math.sin(current_time * 0.5) * 0.3) * (variations - 1)) % variations
    rgb_color = cs.lab_to_rgb(lab_colors[color_index])
    
    return [c / 255.0 for c in rgb_color]    
    
class LazyEye():
    def __init__(self, bl_: blType, movingType_):
        self.bl = bl_
        self.movingType = movingType_
    def run(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        #без перспективы (ортографическое представление)
        #gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)

        ground_size = 20.0
        aspect_ratio = display[0] / display[1]
        
        left = -ground_size
        right = ground_size
        bottom = -ground_size / aspect_ratio
        top = ground_size / aspect_ratio
            
        glOrtho(left, right, bottom, top, 0.1, 100.0)
        
        #переключение на модельно-видовую матрицу
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        init_lighting()

        #параметры сцены
        orbit_radius = 8.0
        ball_radius = 1.0
        
        ball_position = [0, 0, 0]
        start_time = time.time()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            set_background_color(self.bl)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            cur_time = time.time() - start_time
            
            ball_position[0], ball_position[1], ball_position[2] = self.movingType(
                cur_time, orbit_radius )
            
            cur_color = calc_cur_color(self.bl, ball_position, 20.0, cur_time)
            
            glLoadIdentity()
            
            glRotatef(90, 1, 0, 0)  # Поворачиваем камеру
            
            # Отодвигаем камеру вверх
            glTranslatef(0.0, -30.0, 0.0)
            
            # Отрисовка сцены
            draw_ground(20.0, self.bl)
            draw_ball(ball_position, ball_radius, cur_color)
            
            
            pygame.display.flip()
            clock.tick(60)
