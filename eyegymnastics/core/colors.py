from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy
from colormath.color_objects import LabColor, sRGBColor
import cv2
from ..enum.bltype import blType
from colorsystem import ColorSystem


def lab_to_rgb(self, color_lab: LabColor):
        try:
            rgb_color = color_lab.convert_to('sRGB')
            
            r = max(0, min(1, rgb_color.rgb_r))
            g = max(0, min(1, rgb_color.rgb_g))
            b = max(0, min(1, rgb_color.rgb_b))
            
            return (int(r * 255), int(g * 255), int(b * 255))
        except:
            # fallback если colormath не работает
            lab_array = numpy.array([[
                [color_lab.lab_l, color_lab.lab_a, color_lab.lab_b]
            ]], dtype=numpy.float32)
            
            bgr_color = cv2.cvtColor(lab_array, cv2.COLOR_LAB2BGR)
            rgb_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2RGB)
            
            r = int(rgb_color[0, 0, 0] * 255)
            g = int(rgb_color[0, 0, 1] * 255)
            b = int(rgb_color[0, 0, 2] * 255)
            
            return (r, g, b)

def generate_colors(self, base_lab: LabColor, variations, x_norm, z_norm, time):
        variations_list = []
        
        for i in range(variations):
            if base_lab.lab_a == 0 and base_lab.lab_b == 0:  # Achromatopsia
                #только вариации яркости
                l_variation = 30 * math.sin(x_norm * math.pi * 2 + i)
                new_l = base_lab.lab_l + l_variation
                new_l = max(20, min(80, new_l))
                new_color = LabColor(new_l, 0, 0)
            else:
                #для цветного зрения - изменяем и оттенки
                angle1 = x_norm * math.pi * 2 + i * math.pi / 2
                angle2 = z_norm * math.pi * 2 + time * 0.3
                
                l_variation = 25 * math.sin(angle1)
                a_variation = 60 * math.cos(angle1 + angle2)
                b_variation = 60 * math.sin(angle2)
                
                new_l = base_lab.lab_l + l_variation
                new_a = base_lab.lab_a + a_variation
                new_b = base_lab.lab_b + b_variation
                
                new_l = max(0, min(100, new_l))
                new_a = max(-100, min(100, new_a))
                new_b = max(-100, min(100, new_b))
                
                new_color = LabColor(new_l, new_a, new_b)
            
            variations_list.append(new_color)
        
        return variations_list



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
        lab_colors = generate_colors(base_color, variations, x_norm, z_norm, current_time)
        
        color_index = int((x_norm + math.sin(current_time * 0.5) * 0.3) * (variations - 1)) % variations
        rgb_color = lab_to_rgb(lab_colors[color_index])
        
        return [c / 255.0 for c in rgb_color]    
