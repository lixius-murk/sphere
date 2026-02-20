import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.render.render import EyeGymnasticsOne, EyeGymnasticsTwo
from enumData.bltype import blType
from src.render import movements

def launch_app():
    user_vision = blType.Deuteranopia
    selected_movement = movements.calc_cur_coordinates_circle_right
    app = EyeGymnasticsOne(bl_type=user_vision, movement_func=selected_movement)
    
    try:
        print(f"Starting session for {user_vision.name}...")
        app.run()
    except Exception as e:
        print(f"Application failed to start: {e}")

if __name__ == "__main__":
    launch_app()