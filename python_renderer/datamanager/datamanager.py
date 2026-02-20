import time
import datetime
import json
import os
import logging
from pythonjsonlogger import jsonlogger
from pathlib import Path
from enumData.bltype import blType

class DataManager:
    def __init__(self, data_dir: str = "data"):
        base_path = Path(__file__).parent.parent.parent
        self.data_dir = base_path / data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.start_timestamp = None
        self.frame_count = 0
        self.coordinates_buffer = []
        self.session_data = {}
        
        self._setup_logger()
        
    def _setup_logger(self):
        self.logger = logging.getLogger("EyeGymnastics")
        self.logger.setLevel(logging.INFO)
        
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        log_file = self.data_dir / "gymnastics.log"
        handler = logging.FileHandler(filename=log_file, encoding='utf-8')
        
        formatter = jsonlogger.JsonFormatter(
            fmt='%(asctime)s %(levelname)s %(session_id)s %(bl_type)s %(movement)s %(duration).2f %(x_coord).3f %(y_coord).3f %(error_msg)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def start_session(self, bl_type: blType, mv: str):
        self.start_timestamp = time.time()
        self.frame_count = 0
        self.coordinates_buffer = []
        
        session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.session_data = {
            "session_id": session_id,
            "color_blindness_type": bl_type.name,
            "movement_function": mv,
            "session_start": datetime.datetime.now().isoformat(),
            "completion_status": "started"
        }
        
        self.logger.info(
            "Session started",
            extra={
                'session_id': session_id,
                'bl_type': bl_type.name,
                'movement': mv,
                'duration': 0,
                'x_coord': 0,
                'y_coord': 0,
                'error_msg': ''
            }
        )
        
        return self.session_data.copy()

    def log_coordinates(self, coord):
        if not self.start_timestamp:
            return
        
        current_time = time.time() - self.start_timestamp
        self.frame_count += 1
        
        self.coordinates_buffer.append({
            'time': round(current_time, 3),
            'x': round(coord[0], 3),
            'y': round(coord[1], 3),
        })
        
        if len(self.coordinates_buffer) > 1000:
            self.flush_coordinates_buffer()
        
        if self.frame_count % 10 == 0:
            self.logger.info(
                "Coordinates",
                extra={
                    'session_id': self.session_data.get('session_id', 'unknown'),
                    'bl_type': self.session_data.get('color_blindness_type', 'unknown'),
                    'movement': self.session_data.get('movement_function', 'unknown'),
                    'duration': current_time,
                    'x_coord': coord[0],
                    'y_coord': coord[1],
                    'error_msg': ''
                }
            )
    
    def add_error(self, error: Exception):
        error_msg = f"{type(error).__name__}: {str(error)}"
        
        self.logger.error(
            "Error",
            extra={
                'session_id': self.session_data.get('session_id', 'unknown'),
                'bl_type': self.session_data.get('color_blindness_type', 'unknown'),
                'movement': self.session_data.get('movement_function', 'unknown'),
                'duration': time.time() - self.start_timestamp if self.start_timestamp else 0,
                'x_coord': 0,
                'y_coord': 0,
                'error_msg': error_msg
            },
            exc_info=True
        )
    
    def flush_coordinates_buffer(self):
        if not self.coordinates_buffer:
            return
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        coords_file = self.data_dir / f"coords_{timestamp}.json"
        
        with open(coords_file, 'w', encoding='utf-8') as f:
            json.dump(self.coordinates_buffer, f, ensure_ascii=False, indent=2)
        
        self.coordinates_buffer.clear()
    
    def end_session(self, session_data: dict):
        if self.start_timestamp:
            duration = time.time() - self.start_timestamp
        else:
            duration = 0
        
        self.flush_coordinates_buffer()
        
        self.logger.info(
            "Session ended",
            extra={
                'session_id': session_data.get('session_id', 'unknown'),
                'bl_type': session_data.get('color_blindness_type', 'unknown'),
                'movement': session_data.get('movement_function', 'unknown'),
                'duration': duration,
                'x_coord': 0,
                'y_coord': 0,
                'error_msg': ''
            }
        )
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.data_dir / f"session_{timestamp}.json"
        
        session_data.update({
            "session_end": datetime.datetime.now().isoformat(),
            "duration_seconds": round(duration, 2),
            "total_frames": self.frame_count
        })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)
        
        return session_data