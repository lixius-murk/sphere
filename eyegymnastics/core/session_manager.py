import time
import datetime
import json
import os
from typing import Dict, Any
from ..enum.bltype import ColorBlindnessType


class SessionManager:
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def start_session(self, bl_type: ColorBlindnessType, movement_func_name: str) -> Dict[str, Any]:
        session_data = {
            "bl_type": bl_type.name,
            "movement_function": movement_func_name,
            "session_start": datetime.datetime.now().isoformat(),
            "session_start_timestamp": time.time(),
            "completion_status": "started",
        }
        return session_data
    
    def end_session(self, session_data: Dict[str, Any]):
        session_data["session_end"] = datetime.datetime.now().isoformat()
        session_data["session_end_timestamp"] = time.time()
        
        if "session_start_timestamp" in session_data:
            duration = session_data["session_end_timestamp"] - session_data["session_start_timestamp"]
            session_data["duration_seconds"] = duration
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.data_dir, f"session_{timestamp}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)
        
        return session_data
