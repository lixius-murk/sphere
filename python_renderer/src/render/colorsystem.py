import math
import numpy
import cv2
from colormath.color_objects import LabColor, sRGBColor
from OpenGL.GL import *
from enumData.bltype import blType

class ColorSystem:
    def __init__(self):
        self.base_palettes = {
            blType.Healthy: {
                'primary': LabColor(60, 40, 40),
                'secondary': LabColor(60, -40, 60),
                'accent': LabColor(50, 20, -60),
            },
            blType.Deuteranopia: {
                'primary': LabColor(65, 50, 30),
                'secondary': LabColor(55, -10, -50),
                'accent': LabColor(70, -20, 0),
            },
            blType.Protanopia: {
                'primary': LabColor(60, 20, 50),
                'secondary': LabColor(55, -30, 10),
                'accent': LabColor(45, 10, -40),
            },
            blType.Tritanopia: {
                'primary': LabColor(60, 60, 10),
                'secondary': LabColor(60, -40, 10),
                'accent': LabColor(40, 30, -20),
            },
            blType.Achromatopsia: {
                'primary': LabColor(40, 0, 0),
                'secondary': LabColor(65, 0, 0),
                'accent': LabColor(80, 0, 0),
            }
        }

    def get_base_color(self, blindness_type: blType, color_type='primary'):
        return self.base_palettes.get(blindness_type, self.base_palettes[blType.Healthy])[color_type]

    def lab_to_rgb(self, color_lab: LabColor):
        try:
            rgb_color = color_lab.convert_to('sRGB')
            return (rgb_color.rgb_r, rgb_color.rgb_g, rgb_color.rgb_b)
        except:
            lab_array = numpy.array([[[color_lab.lab_l, color_lab.lab_a, color_lab.lab_b]]], dtype=numpy.float32)
            bgr_color = cv2.cvtColor(lab_array, cv2.COLOR_LAB2BGR)
            rgb = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2RGB)[0][0]
            return (rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)

    def generate_colors(self, base_lab: LabColor, variations, x_norm, z_norm, time_val):
        variations_list = []
        for i in range(variations):
            if base_lab.lab_a == 0 and base_lab.lab_b == 0:
                l_var = 30 * math.sin(x_norm * math.pi * 2 + i)
                new_color = LabColor(max(20, min(80, base_lab.lab_l + l_var)), 0, 0)
            else:
                angle1 = x_norm * math.pi * 2 + i * math.pi / 2
                angle2 = z_norm * math.pi * 2 + time_val * 0.3
                new_color = LabColor(
                    max(0, min(100, base_lab.lab_l + 25 * math.sin(angle1))),
                    max(-100, min(100, base_lab.lab_a + 60 * math.cos(angle1 + angle2))),
                    max(-100, min(100, base_lab.lab_b + 60 * math.sin(angle2)))
                )
            variations_list.append(new_color)
        return variations_list

    def calc_cur_color(self, bl: blType, ball_position, ground_size, current_time):
    # DONT DO THIS: cs = ColorSystem() 
    # Use 'self' instead to use the existing palette
    
        variations = 8
        x_norm = (ball_position[0] + ground_size) / (2 * ground_size)
        z_norm = (ball_position[2] + ground_size) / (2 * ground_size)
        
        # Determine which base color to use
        color_type = 'primary'
        if bl == blType.Deuteranopia: color_type = 'secondary'
        elif bl == blType.Protanopia: color_type = 'accent'
        
        # Get the base color from the instance's own palette
        base_color = self.get_base_color(bl, color_type)
        
        # Generate the variation list based on the MOVING time
        lab_colors = self.generate_colors(base_color, variations, x_norm, z_norm, current_time)
        
        # Select index based on position and time
        color_index = int((x_norm + math.sin(current_time * 0.5) * 0.3) * (variations - 1)) % variations
        rgb_color = self.lab_to_rgb(lab_colors[color_index])
        
        return rgb_color

    @staticmethod
    def set_background_color(bl_type: blType):
        if bl_type == blType.Achromatopsia:
            glClearColor(0.9, 0.9, 0.9, 1.0)
        else:
            glClearColor(0.2, 0.2, 0.3, 1.0)