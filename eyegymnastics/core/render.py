import pygame
import math
import time
import json
import datetime
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from colors import ColorSystem
from ..enum.bltype import blType
from eyegymnastics.util.dataload import writeData
import colors 



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




class EyeGymnastics():
    def __init__(self, bl_: blType, movingType_):
        self.bl = bl_
        self.movingType = movingType_
        self.session_data = None
    def run(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    def set_session_data(self, session_data):
        program_end_datetime = datetime.datetime.now()
        program_end_time = time.time()
        
        session_data["session_end"] = program_end_datetime.now(datetime.timezone.utc).isoformat()
        session_data["session_end_timestamp"] = program_end_time
        
        if "session_start_timestamp" in session_data:
            session_data["session_duration_seconds"] = program_end_time - session_data["session_start_timestamp"]
            
        
        return session_data

class EyeGymnasticsOne(EyeGymnastics):
    def __init__(self, bl_: blType, movingType_):
        super().__init__(bl_, movingType_)  
    def run(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        session_data = {
            "blType_name": self.bl.name,
            "movement_function_name": self.movingType.__name__,
            "session_start": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "session_start_timestamp": time.time(),
            "session_end": None,
            "session_end_timestamp": None,
        }
        try:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            
            #без перспективы (ортографическое представление)
            #gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)

            ground_size = 15.0
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
            speed = 2.0
            
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
                    cur_time, orbit_radius, ground_size, speed)
                
                cur_color = calc_cur_color(self.bl, ball_position, 20.0, cur_time)
                
                glLoadIdentity()
                
                glRotatef(90, 1, 0, 0)  # Поворачиваем камеру
                
                # Отодвигаем камеру вверх
                glTranslatef(0.0, -20.0, 0.0)
                
                # Отрисовка сцены
                draw_ground(20.0, self.bl)
                draw_ball(ball_position, ball_radius, cur_color)
                
                
                pygame.display.flip()
                clock.tick(60)
            
        except Exception as e:
            print(f"\nОшибка: {e}")
            
        finally:
            session_data = self.set_session_data(session_data)
            writeData(session_data)
                
class EyeGymnasticsTwo(EyeGymnastics):
    def __init__(self, bl_: blType, movingType_):
        super().__init__(bl_, movingType_)  
    def run(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        session_data = {
            "blType_name": self.bl.name,
            "movement_function_name": self.movingType.__name__,
            "session_start": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "session_start_timestamp": time.time(),
            "session_end": None,
            "session_end_timestamp": None,
        }
        try:
            pygame.init()
            display = (800, 600)
            pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
            
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            
            #без перспективы (ортографическое представление)
            #gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)

            ground_size = 15.0
            aspect_ratio = display[0] / display[1]
            
            left = -ground_size
            right = ground_size
            bottom = -ground_size / aspect_ratio
            top = ground_size / aspect_ratio
                
            glOrtho(left, right, bottom, top, 0.1, 100.0)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            
            #без перспективы (ортографическое представление)
            #gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)

            ground_size = 15.0
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
            speed = 2.0
            
            ball_position_one = [0, 0, 0]
            ball_position_two = [0, 0, 0]
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
                
                ball_position_one[0], ball_position_one[1], ball_position_one[2] = self.movingType(
                    cur_time, orbit_radius, ground_size, speed )
                
                ball_position_two[0], ball_position_two[1], ball_position_two[2] = self.movingType(
                    cur_time, orbit_radius, ground_size, speed )
                ball_position_two[0] = - ball_position_two[0]
                
                cur_color_one = calc_cur_color(self.bl, ball_position_one, 20.0, cur_time)
                cur_color_two = calc_cur_color(self.bl, ball_position_two, 20.0, cur_time)

                
                glLoadIdentity()
                
                glRotatef(90, 1, 0, 0)  # Поворачиваем камеру
                
                # Отодвигаем камеру вверх
                glTranslatef(0.0, -20.0, 0.0)
                
                # Отрисовка сцены
                draw_ground(20.0, self.bl)
                draw_ball(ball_position_one, ball_radius, cur_color_one)
                draw_ball(ball_position_two, ball_radius, cur_color_two)

                
                
                pygame.display.flip()
                clock.tick(60)
            
        except Exception as e:
            print(f"\nОшибка: {e}")
            
        finally:
            session_data = self.set_session_data(session_data)
            writeData(session_data)
    