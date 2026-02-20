import mmap
import struct
from win32.lib import win32con 
import win32.win32api as win32api
import struct
import struct
import mmap
import time

CTRL_FMT = "IIII"
CTRL_SIZE = struct.calcsize(CTRL_FMT)

FMT_RGB = 0


import struct
import mmap
import time

CTRL_FMT = "IIII"
CTRL_SIZE = struct.calcsize(CTRL_FMT)

FMT_RGB = 0

class SharedFrameWriter:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.frame_size = w * h * 3
        self.frame_id = 0

        print(f"Creating shared memory for {w}x{h} (size: {self.frame_size} bytes)")
        
        try:
            # Try to create new shared memory
            self.ctrl_buf = mmap.mmap(-1, CTRL_SIZE, tagname="ctrl")
            print(f"Created CTRL shared memory, size: {CTRL_SIZE}")
            
            self.frame_buf = mmap.mmap(-1, self.frame_size, tagname="frame")
            print(f"Created FRAME shared memory, size: {self.frame_size}")
            
            # Initialize control block with zeros
            self.ctrl_buf.seek(0)
            self.ctrl_buf.write(struct.pack(CTRL_FMT, w, h, FMT_RGB, 0))
            self.ctrl_buf.flush()
            
            print("Shared memory created and initialized successfully")
        except PermissionError as e:
            print(f"Permission error: {e}")
            # If it exists, try to open existing
            print("Trying to open existing shared memory...")
            self.ctrl_buf = mmap.mmap(0, CTRL_SIZE, tagname="ctrl")
            self.frame_buf = mmap.mmap(0, self.frame_size, tagname="frame")
            print("Opened existing shared memory")

    def write_raw(self, rgb_bytes: bytes):
        if len(rgb_bytes) != self.frame_size:
            raise ValueError(f"Frame size mismatch: expected {self.frame_size}, got {len(rgb_bytes)}")

        # Write frame data
        self.frame_buf.seek(0)
        self.frame_buf.write(rgb_bytes)
        self.frame_buf.flush()  # Force write to memory

        self.frame_id += 1

        # Write control block
        self.ctrl_buf.seek(0)
        self.ctrl_buf.write(struct.pack(
            CTRL_FMT,
            self.w,
            self.h,
            FMT_RGB,
            self.frame_id
        ))
        self.ctrl_buf.flush()  # Force write to memory
        
        print(f"Wrote frame {self.frame_id}")  # Debug each frame

# class SharedFrameWriter:
#     def __init__(self, w, h):
#         self.w = w
#         self.h = h
#         self.frame_size = w * h * 3
#         self.frame_id = 0

#         try:
#             # Try to create new shared memory
#             self.ctrl_buf = mmap.mmap(-1, CTRL_SIZE, tagname="ctrl")
#             self.frame_buf = mmap.mmap(-1, self.frame_size, tagname="frame")
#             print("Shared memory created successfully")
#         except PermissionError:
#             # If it exists, try to open existing
#             print("Shared memory might already exist, trying to open...")
#             self.ctrl_buf = mmap.mmap(0, CTRL_SIZE, tagname="ctrl")
#             self.frame_buf = mmap.mmap(0, self.frame_size, tagname="frame")
#             print("Opened existing shared memory")

#     def write_raw(self, rgb_bytes: bytes):
#         if len(rgb_bytes) != self.frame_size:
#             raise ValueError(f"Frame size mismatch: expected {self.frame_size}, got {len(rgb_bytes)}")

#         # Write frame data
#         self.frame_buf.seek(0)
#         self.frame_buf.write(rgb_bytes)

#         self.frame_id += 1

#         # Write control block
#         self.ctrl_buf.seek(0)
#         self.ctrl_buf.write(struct.pack(
#             CTRL_FMT,
#             self.w,
#             self.h,
#             FMT_RGB,
#             self.frame_id
#         ))
#         print(f"Wrote frame {self.frame_id}")  # Debug