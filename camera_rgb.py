from picamera2 import Picamera2
import time

def open_rgb_camera():
    cam = Picamera2()
    cam.start()
    time.sleep(1)
    return cam

def capture_rgb_frame(cam):
    return cam.capture_array()
