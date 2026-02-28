import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.render.render import EyeGymnasticsOne, EyeGymnasticsTwo
from enumData.bltype import blType
from src.render import movements
import src.render.movements 

def launch_app(argv):
    if(len(argv) != 4):
        print(f"Wrong amount of arguments:  {argv}")
        return
    user_vision = blType[argv[2]]  
    selected_movement = src.render.movements.movements[argv[3]]
    
    if(argv[1] == "1"):
        app = EyeGymnasticsOne(bl_type=user_vision, movement_func=selected_movement)
    else:        
        app = EyeGymnasticsTwo(bl_type=user_vision, movement_func=selected_movement)
    
    try:
        print(f"Starting session for {user_vision.name}...")
        app.run()
    except Exception as e:
        print(f"Application failed to start: {e}")

if __name__ == "__main__":
    launch_app(sys.argv)