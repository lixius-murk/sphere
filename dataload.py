import os
import json
from datetime  import datetime, timedelta 
from typing import Dict, Any


def writeData(data: Dict[str, Any]):
    os.makedirs('data', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/session_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
