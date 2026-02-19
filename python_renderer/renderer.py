import sys
import os

#todo:проверить корректность директории(!)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.render.render import EyeGymnasticsOne
from src.enum.bltype import blType
from src.render import movements

def launch_app():

    user_vision = blType.Deuteranopia
    selected_movement = movements.calc_cur_coordinates_circle_right
    #todo: реализовать передачу данных
    app = EyeGymnasticsOne(
        bl_type=user_vision, 
        movement_func=selected_movement
    )
    
    try:
        print(f"Starting session for {user_vision.name}...")
        
        app.run()
        print("Shared memory created:", self.ctrl.name, self.frame.name, flush=True)

    except Exception as e:
        print(f"Application failed to start: {e}")

if __name__ == "__main__":
    launch_app()