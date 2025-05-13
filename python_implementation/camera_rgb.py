import cv2
import time
from picamera2 import Picamera2

def open_rgb_camera():
    cam = Picamera2()
    cam.start()
    time.sleep(1)
    return cam

def capture_rgb_frame(cam):
    return cam.capture_array()

if __name__ == "__main__":
    cam = open_rgb_camera()
    print("RGB camera opened and started successfully.")

    while True:
        rgb_frame = capture_rgb_frame(cam)
        print("Captured RGB frame shape:", rgb_frame.shape)

        # If frame has 4 channels (BGRA), convert to BGR for correct display
        if rgb_frame.shape[2] == 4:
            rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGRA2BGR)

        cv2.imshow("RGB Camera View", rgb_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cam.close()
    cv2.destroyAllWindows()
