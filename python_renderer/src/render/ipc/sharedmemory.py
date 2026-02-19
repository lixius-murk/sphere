import struct
from multiprocessing import shared_memory

CTRL_FMT = "IIII"
CTRL_SIZE = struct.calcsize(CTRL_FMT)

FMT_RGB = 0  # просто enum

_ctrl = None
_frame = None

class SharedFrameWriter:
    def __init__(self, w, h):
        global _ctrl, _frame

        self.w = w
        self.h = h
        self.frame_size = w * h * 3
        self.frame_id = 0

        if _ctrl is None:
            _ctrl = shared_memory.SharedMemory(
                name="ctrl",
                create=True,
                size=CTRL_SIZE
            )

        if _frame is None:
            _frame = shared_memory.SharedMemory(
                name="frame",
                create=True,
                size=self.frame_size
            )

        self.ctrl = _ctrl
        self.frame = _frame

        print("Shared memory created:")
        print("CTRL:", self.ctrl.name)
        print("FRAME:", self.frame.name)

    def write_raw(self, rgb_bytes: bytes):
        if len(rgb_bytes) != self.frame_size:
            raise ValueError(
                f"Frame size mismatch: {len(rgb_bytes)} != {self.frame_size}"
            )

        # пишем frame
        self.frame.buf[:self.frame_size] = rgb_bytes

        # обновляем ctrl block
        self.frame_id += 1
        struct.pack_into(
            CTRL_FMT,
            self.ctrl.buf,
            0,
            self.w,
            self.h,
            FMT_RGB,
            self.frame_id
        )
