import struct
from multiprocessing import shared_memory

class SharedFrameWriter:
    CTRL_NAME = "ctrl"
    FRAME_NAME = "frame"
    FMT_RGB = 0

    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self.frame_size = self.w * self.h * 3

        try:
            self.ctrl = shared_memory.SharedMemory(
                name=self.CTRL_NAME,
                create=True,
                size=16
            )
        except FileExistsError:
            self.ctrl = shared_memory.SharedMemory(
                name=self.CTRL_NAME,
                create=False
            )

        try:
            self.frame = shared_memory.SharedMemory(
                name=self.FRAME_NAME,
                create=True,
                size=self.frame_size
            )
        except FileExistsError:
            self.frame = shared_memory.SharedMemory(
                name=self.FRAME_NAME,
                create=False
            )

        self.frame_id = 0
        
    
    def write_raw(self, rgb_bytes: bytes):
        if len(rgb_bytes) != self.frame_size:
            raise ValueError("Frame size mismatch")

        self.frame.buf[:self.frame_size] = rgb_bytes
        self.frame_id += 1
        struct.pack_into(
            "IIII",
            self.ctrl.buf,
            0,
            self.w,
            self.h,
            self.FMT_RGB,
            self.frame_id
        )