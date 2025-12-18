import json
import os
from datetime import datetime
from typing import Dict, Any

def save_session_data(data: Dict[str, Any], data_dir: str = "data"):
    os.makedirs(data_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(data_dir, f"session_{timestamp}.json")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return filename

def load_session_data(filename: str) -> Dict[str, Any]:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
