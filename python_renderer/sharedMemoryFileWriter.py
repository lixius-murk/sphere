import mmap
import struct
import os
import numpy as np

import mmap
import struct
import os
import sys
import time

class SharedMemoryWriter:
    def __init__(self, name="frames", width=800, height=600):
        self.name = name
        self.width = width
        self.height = height
        self.frame_size = width * height * 3
        self.buffer_size = self.frame_size + 5  # 5 bytes for counter
        self.frame_id = 0

        if sys.platform == "win32":
            # Windows: use a named memory-mapped file with a "Global\" prefix
            # to allow access across sessions (no admin rights needed)
            self.map_file = mmap.mmap(-1, self.buffer_size,
                                      tagname=f"Global\\{name}")
        else:
            # Linux / macOS: use a file in /dev/shm/
            self.path = f"/dev/shm/{name}"
            # Remove stale segment
            try:
                os.unlink(self.path)
            except FileNotFoundError:
                pass
            with open(self.path, "wb") as f:
                f.write(b"\0" * self.buffer_size)
            self.fd = os.open(self.path, os.O_RDWR)
            self.map_file = mmap.mmap(self.fd, self.buffer_size,
                                      mmap.MAP_SHARED)

        # Initialise with zeros
        self.map_file.seek(0)
        self.map_file.write(b"\0" * self.buffer_size)
        self.map_file.flush()
        print(f"✅ Shared memory '{name}' ready ({self.buffer_size} bytes)")

    def write_frame(self, rgb_bytes):
        if len(rgb_bytes) != self.frame_size:
            return
        self.map_file.seek(4)
        self.map_file.write(struct.pack("B", 1))   #writing = true
        self.map_file.flush()

        self.map_file.seek(5)
        self.map_file.write(rgb_bytes)

        self.map_file.seek(0)
        self.map_file.write(struct.pack("I", self.frame_id))  #update counter
        self.map_file.seek(4)
        self.map_file.write(struct.pack("B", 0))   #writing = false
        self.map_file.flush()

        self.frame_id += 1

    def close(self):
        self.map_file.close()
        if hasattr(self, "fd"):
            os.close(self.fd)
        if hasattr(self, "path") and os.path.exists(self.path):
            os.unlink(self.path)

