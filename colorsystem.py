

import math
import numpy
from colormath.color_objects import LabColor, sRGBColor
import cv2
from bltype import blType

class ColorSystem:
    def __init__(self):
        self.base_palettes = {
            blType.Healthy: {
                'primary': LabColor(60, 40, 40),      # красно-оранжевый
                'secondary': LabColor(60, -40, 60),   # яркий зеленый
                'accent': LabColor(50, 20, -60),      # глубокий синий
                'background': LabColor(100, 0, 0),     # почти белый
            },
            blType.Deuteranopia: {
                'primary': LabColor(65, 50, 30),      # оранжево-коричневый (видимый)
                'secondary': LabColor(55, -10, -50),  # сине-фиолетовый (видимый)
                'accent': LabColor(70, -20, 0),       # голубовато-серый
                'background': LabColor(100, 0, 0),
            },
            blType.Protanopia: {
                'primary': LabColor(60, 20, 50),      # розово-фиолетовый (видимый)
                'secondary': LabColor(55, -30, 10),   # бирюзово-зеленый
                'accent': LabColor(45, 10, -40),      # темно-синий
                'background': LabColor(100, 0, 0),
            },
            blType.Tritanopia: {
                'primary': LabColor(60, 60, 10),      # красно-оранжевый
                'secondary': LabColor(60, -40, 10),   # зеленоватый
                'accent': LabColor(40, 30, -20),      # пурпурно-синий
                'background': LabColor(100, 0, 0),
            },
            blType.Achromatopsia: {
                'primary': LabColor(40, 0, 0),        # темно-серый
                'secondary': LabColor(65, 0, 0),      # серый
                'accent': LabColor(80, 0, 0),         # светло-серый
                'background': LabColor(100, 0, 0),
            }
        }

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
                # Только вариации яркости
                l_variation = 30 * math.sin(x_norm * math.pi * 2 + i)
                new_l = base_lab.lab_l + l_variation
                new_l = max(20, min(80, new_l))
                new_color = LabColor(new_l, 0, 0)
            else:
                # Для цветного зрения - изменяем и оттенки
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

    def get_palette_colors(self, blindness_type: blType, color_type='primary', variations=3):
        base_color = self.base_palettes[blindness_type][color_type]
        return self.generate_colors_variative(base_color, variations, 0.5, 0.5, 0)
    
    def get_base_color(self, blindness_type: blType, color_type='primary'):
        return self.base_palettes[blindness_type][color_type]   

