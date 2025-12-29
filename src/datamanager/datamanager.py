import time
import datetime
import json
import os
from ..enum.bltype import blType

class DataManager:
    def __init__(self, data_dir: str = "data"):
        # Get absolute path relative to the project root
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(base_path, data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        self.start_timestamp = None

    def start_session(self, bl_type: blType, mv: str):
        self.start_timestamp = time.time()
        session_data = {
            "color_blindness_type": bl_type.name,
            "movement_function": mv,
            "session_start": datetime.datetime.now().isoformat(),
            "completion_status": "started",
        }
        return session_data

    def end_session(self, session_data: dict):
        if self.start_timestamp:
            duration = time.time() - self.start_timestamp
        else:
            duration = 0

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.data_dir, f"session_{timestamp}.json")

        session_data.update({
            "session_end": datetime.datetime.now().isoformat(),
            "duration_seconds": round(duration, 2),
        })

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)