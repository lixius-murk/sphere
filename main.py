import os
import sys
import pygame
from lazyeye import LazyEyeOne, LazyEyeTwo
from bltype import blType
import math


def calc_cur_coordinates_circle_right(current_time, orbit_radius, ground_sz, orbit_speed=1.0):
    angle = current_time * orbit_speed
    #x = center + radius * cos(time) y = center + radius * sin(time)
    x = orbit_radius * math.cos(angle)
    z = orbit_radius * math.sin(angle)
    y = 0.5  
    
    return x, y, z

def calc_cur_coordinates_circle_left(current_time, orbit_radius, ground_sz, orbit_speed=1.0):
    angle = current_time * orbit_speed
    #x = center + radius * cos(time) y = center + radius * sin(time)
    x = orbit_radius * math.cos(angle)
    z = orbit_radius * math.sin(angle)
    y = 0.5  
    
    return -x, y, z

#от парвый верхний в левого нижнего
def calc_cur_coordinates_diagonal_down(current_time, orbit_radius, ground_sz, speed=1.0):
    angle = current_time * speed
    val =  math.sin(angle) * (ground_sz/2)
    y = 0.5
    
    return val, y, val


#от левого нижнего в парвый верхний не сдвигом фазы, а просто -
def calc_cur_coordinates_diagonal_up(current_time, orbit_radius, ground_sz, speed=1.0):
    angle = current_time * speed
    val =  math.sin(angle) * (ground_sz/2)
    y = 0.5
    return -val, y, val

def calc_cur_coordinates_hotizontal(current_time, orbit_radius, ground_sz, speed=1.0):
    angle = current_time * speed
    z = math.sin(angle)*ground_sz
    y = 0.5
    x = 0
    
    return x, y, z

def calc_cur_coordinates_vertical(current_time, orbit_radius, ground_sz,  speed=1.0):
    angle = current_time * speed
    x = math.sin(angle)*ground_sz
    y = 0.5
    z = 0
    
    return x, y, z

def calc_cur_coordinates_zigzag(current_time, orbit_radius, ground_sz, speed):
    y = 0.5
    t = current_time * speed /3

    # период зиг-зага (вперёд + назад)
    period = 1.0
    phase = (t % period) / period  # 0..1

    # пилообразная форма: 0→1→0→1→…
    saw = 2 * abs(phase - 0.5)

    # движение от -ground_sz/2 до +ground_sz/2 и обратно
    z = (saw - 0.5) * ground_sz

    x = orbit_radius * math.sin(t)

    return x, y, z

def calc_cur_coordinates_clock(current_time, orbit_radius, ground_sz, speed):
    y = 0.5
    #вариант с автоматом или с парсированием врмемени
    MOVE_TIME = 2.0
    STOP_TIME = 1.0
    CYCLE_TIME = 12.0
    
    t = current_time * speed
    cycle_time = t % CYCLE_TIME
    
    if cycle_time < MOVE_TIME:
        #  1: Движение от 9 к 12 часам
        progress = cycle_time / MOVE_TIME
        angle = math.pi + progress * (math.pi/2)  # π → 3π/2
        
    elif cycle_time < MOVE_TIME + STOP_TIME:
        #  2: Остановка на 12 часах
        angle = 3 * math.pi / 2  # 270°
        
    elif cycle_time < 2*MOVE_TIME + STOP_TIME:
        #  3: Движение от 12 к 3 часам
        segment_time = cycle_time - (MOVE_TIME + STOP_TIME)
        progress = segment_time / MOVE_TIME
        angle = 3*math.pi/2 + progress * (math.pi/2)  # 3π/2 → 2π (0)
        
    elif cycle_time < 2*MOVE_TIME + 2*STOP_TIME:
        #  4: Остановка на 3 часах
        angle = 0  # 0°
        
    elif cycle_time < 3*MOVE_TIME + 2*STOP_TIME:
        #  5: Движение от 3 к 6 часам
        segment_time = cycle_time - (2*MOVE_TIME + 2*STOP_TIME)
        progress = segment_time / MOVE_TIME
        angle = 0 + progress * (math.pi/2)  # 0 → π/2
        
    elif cycle_time < 3*MOVE_TIME + 3*STOP_TIME:
        #  6: Остановка на 6 часах
        angle = math.pi / 2  # 90°
        
    elif cycle_time < 4*MOVE_TIME + 3*STOP_TIME:
        #  7: Движение от 6 к 9 часам
        # Движение: по часовой стрелке на 90°
        segment_time = cycle_time - (3*MOVE_TIME + 3*STOP_TIME)
        progress = segment_time / MOVE_TIME
        angle = math.pi/2 + progress * (math.pi/2)  # π/2 → π
        
    else:
        #  8: Остановка на 9 часах
        angle = math.pi  # 180°
    
    #угол в диапазон 0-2π
    angle = angle % (2 * math.pi)
    
    x = orbit_radius * math.cos(angle)
    z = orbit_radius * math.sin(angle)
    
    return x, y, z

def calc_cur_coordinates_two_diagonals(current_time, orbit_radius, ground_sz, speed):
    y = 0.5
    t = current_time
    
    #цикл по 12 секунд, по 6 на сторону
    period_num = int(t) % 12
    
    angle = t * math.pi 
    val = math.sin(angle) * (ground_sz/2)
    
    if period_num < 6:
        return -val, y, val
    else:
        return val, y, val


def calc_cur_coordinates_rectangle(current_time, orbit_radius, ground_sz, speed):
    y = 0.5
    t = current_time * speed
    cycle_duration = 16.0
    cycle_time = t % cycle_duration
    
    if cycle_time < 4.0:
        # Сторона 1: правый край, сверху вниз
        progress = cycle_time / 4.0  # от 0 до 1
        x = ground_sz / 2
        z = ground_sz/2 - progress * ground_sz  # от ground_sz/2 до -ground_sz/2
        
    elif cycle_time < 8.0:
        # Сторона 2: нижний край, справа налево
        progress = (cycle_time - 4.0) / 4.0  # от 0 до 1
        z = -ground_sz / 2
        x = ground_sz/2 - progress * ground_sz  # от ground_sz/2 до -ground_sz/2
        
    elif cycle_time < 12.0:
        # Сторона 3: левый край, снизу вверх
        progress = (cycle_time - 8.0) / 4.0  # от 0 до 1
        x = -ground_sz / 2
        z = -ground_sz/2 + progress * ground_sz  # от -ground_sz/2 до ground_sz/2
        
    else:  # cycle_time < 16.0
        # Сторона 4: верхний край, слева направо
        progress = (cycle_time - 12.0) / 4.0  # от 0 до 1
        z = ground_sz / 2
        x = -ground_sz/2 + progress * ground_sz  # от -ground_sz/2 до ground_sz/2
    
    return x, y, z

def main():
    m = LazyEyeOne(blType.Achromatopsia, calc_cur_coordinates_rectangle)
    
    m.run()  

# class ModulOne():
#     def __init__(self, bl_: blType):
#         self.bl = bl_
    
#     def run(self):
#         pygame.init()
#         display = (800, 600)
#         pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
#         gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
#         glTranslatef(0.0, 0.0, -50)
#         glEnable(GL_NORMALIZE)
#         glEnable(GL_DEPTH_TEST)
#         init_lighting()

#         bound_sz = 20.0
#         speed = 5.0
#         cur_radius = 2.0
#         ball_position = [0, 0, 0]
#         ball_speed = [0.05*speed, 0*speed, 0.03*speed]
#         bounds = [-bound_sz, bound_sz, -bound_sz, bound_sz]

#         start_time = time.time()
#         clock = pygame.time.Clock()

#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return
            
#             set_background_color(self.bl)
#             glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
#             cur_time = time.time() - start_time

#             ball_position[0] += ball_speed[0]
#             ball_position[2] += ball_speed[2]

#             if ball_position[0] < bounds[0] or ball_position[0] > bounds[1]:
#                 ball_speed[0] = -ball_speed[0]
#             if ball_position[2] < bounds[2] or ball_position[2] > bounds[3]:
#                 ball_speed[2] = -ball_speed[2]

#             cur_color = calc_cur_color(self.bl, ball_position, bound_sz, cur_time)
#             ball_position[1] = cur_radius - 1

#             glPushMatrix()
#             glRotatef(90, bound_sz/2, 0, 0)
#             #draw_ground(bound_sz + 5.0, self.bl)
            
#             draw_ball(ball_position, cur_radius, cur_color)
#             glPopMatrix()

#             pygame.display.flip()
#             clock.tick(60)
            


if __name__ == "__main__":
    main()


if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

if __package__ == "":
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)