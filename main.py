import os
import sys
import pygame
from lazyeye import LazyEyeOne, LazyEyeTwo
from bltype import blType
import math


def calc_cur_coordinates_circle(current_time, orbit_radius, ground_sz, orbit_speed=1.0):
    angle = current_time * orbit_speed
    #x = center + radius * cos(time) y = center + radius * sin(time)
    x = orbit_radius * math.cos(angle)
    z = orbit_radius * math.sin(angle)
    y = 0.5  
    
    return x, y, z

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

    #     # Инициализация состояния
    # state = {
    #     'last_time': 0,
    #     'current_pos': 0,  # 0=12, 1=3, 2=6, 3=9
    #     'state': 'stopped',  # 'moving' or 'stopped'
    #     'state_start': 0,
    #     'current_angle': -math.pi/2  # начинаем с 12 часов
    # }
    
    # # Углы для позиций часов
    # clock_angles = [-math.pi/2, 0, math.pi/2, math.pi]
    # stop_time = 1.0
    # moving_time = 2.0
    # def clock_func(current_time, orbit_radius_param, ground_sz, speed):
    #     """Функция движения"""
    #     nonlocal state
        
    #     # Для совместимости используем переданный радиус
    #     radius = orbit_radius_param if orbit_radius_param > 0 else orbit_radius
        
    #     # Инициализация при первом вызове
    #     if state['last_time'] == 0:
    #         state['last_time'] = current_time
    #         state['state_start'] = current_time
        
    #     if state['state'] == 'stopped':
    #         # Проверяем, не пора ли начать движение
    #         if current_time - state['state_start'] >= stop_time:
    #             state['state'] = 'moving'
    #             state['state_start'] = current_time
    #             state['current_pos'] = (state['current_pos'] + 1) % 4
                
    #     elif state['state'] == 'moving':
    #         # Вычисляем прогресс движения
    #         elapsed = current_time - state['state_start']
    #         progress = min(elapsed / move_time, 1.0)
            
    #         # Начальный и конечный углы
    #         start_idx = (state['current_pos'] - 1) % 4
    #         end_idx = state['current_pos']
            
    #         start_angle = clock_angles[start_idx]
    #         end_angle = clock_angles[end_idx]
            
    #         # Корректируем разницу углов
    #         angle_diff = end_angle - start_angle
    #         if angle_diff > math.pi:
    #             angle_diff -= 2 * math.pi
    #         elif angle_diff < -math.pi:
    #             angle_diff += 2 * math.pi
            
    #         # Интерполяция угла
    #         state['current_angle'] = start_angle + angle_diff * progress
            
    #         # Проверяем завершение движения
    #         if progress >= 1.0:
    #             state['state'] = 'stopped'
    #             state['state_start'] = current_time
        
    #     # Обновляем время
    #     state['last_time'] = current_time
        
    #     # Вычисляем координаты
    #     x = radius * math.cos(state['current_angle'])
    #     z = radius * math.sin(state['current_angle'])
    #     y = 0.5
        
    #     return x, y, z
    
    # return clock_func



def main():
    m = LazyEyeOne(blType.Achromatopsia, calc_cur_coordinates_clock)
    
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