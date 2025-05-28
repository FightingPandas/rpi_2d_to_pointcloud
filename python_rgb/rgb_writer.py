from multiprocessing import shared_memory
import cv2
import numpy as np
import time
from picamera2 import Picamera2
import atexit

# Constants
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CHANNELS = 3
SHM_NAME = "psm_1cba8df0"

def open_camera():
    cam = Picamera2()
    cam.start()
    time.sleep(1)
    return cam

# ✅ Clean up any stale shared memory
try:
    existing_shm = shared_memory.SharedMemory(name=SHM_NAME)
    print("⚠️ Existing shared memory found — unlinking it.")
    existing_shm.close()
    existing_shm.unlink()
except FileNotFoundError:
    pass
except Exception as e:
    print(f"⚠️ Shared memory cleanup warning: {e}")

# ✅ Create new shared memory safely
shm = shared_memory.SharedMemory(name=SHM_NAME, create=True, size=FRAME_WIDTH * FRAME_HEIGHT * CHANNELS)
atexit.register(shm.unlink)  # Ensure cleanup on normal exit
cam = open_camera()
print(f"📷 Writing RGB frames to shared memory: {SHM_NAME}")

try:
    while True:
        frame = cam.capture_array()
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        shm_buf = np.ndarray((FRAME_HEIGHT, FRAME_WIDTH, CHANNELS), dtype=np.uint8, buffer=shm.buf)
        shm_buf[:] = frame
        time.sleep(0.03)  # ~30 FPS
except KeyboardInterrupt:
    print("🛑 Stopping...")
finally:
    cam.close()
    shm.close()
