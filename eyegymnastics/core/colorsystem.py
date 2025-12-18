from ..enum.bltype import blType
from colormath.color_objects import LabColor, sRGBColor
import cv2


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
    #этим методом сразу закрываем get на все типы цветов
    def get_base_color(self, blindness_type: blType, color_type='primary'):
        return self.base_palettes[blindness_type][color_type]   

