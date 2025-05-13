import ArducamDepthCamera as ac
import numpy as np
from scipy.spatial.transform import Rotation as R

MAX_DISTANCE = 4000

def open_depth_camera():
    cam = ac.ArducamCamera()
    
    if cam.open(ac.Connection.CSI, 8) != 0:
        raise RuntimeError("Failed to open Arducam depth camera at index 8")
    
    if cam.start(ac.FrameType.DEPTH) != 0:
        cam.close()
        raise RuntimeError("Failed to start Arducam depth camera")

    cam.setControl(ac.Control.RANGE, MAX_DISTANCE)
    return cam

def capture_depth_frame(cam):
    frame = cam.requestFrame(2000)
    if frame is None:
        raise RuntimeError("Failed to capture frame from depth camera")
    return frame.depth_data, frame.confidence_data

def get_intrinsics(cam):
    fx = cam.getControl(ac.Control.INTRINSIC_FX) / 100.0
    fy = cam.getControl(ac.Control.INTRINSIC_FY) / 100.0
    cx = cam.getControl(ac.Control.INTRINSIC_CX) / 100.0
    cy = cam.getControl(ac.Control.INTRINSIC_CY) / 100.0

    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0,  0,  1]])
    return K

def get_extrinsics(cam):
    tx = cam.getControl(ac.Control.EXTRINSIC_TX) / 100.0
    ty = cam.getControl(ac.Control.EXTRINSIC_TY) / 100.0
    tz = cam.getControl(ac.Control.EXTRINSIC_TZ) / 100.0
    rx = cam.getControl(ac.Control.EXTRINSIC_RX) / 100.0
    ry = cam.getControl(ac.Control.EXTRINSIC_RY) / 100.0
    rz = cam.getControl(ac.Control.EXTRINSIC_RZ) / 100.0

    rotation_matrix = R.from_euler("xyz", [rx, ry, rz], degrees=True).as_matrix()

    extrinsic_matrix = np.eye(4)
    extrinsic_matrix[:3, :3] = rotation_matrix
    extrinsic_matrix[:3, 3] = [tx, ty, tz]
    return extrinsic_matrix

# Optional: run this file directly to test
if __name__ == "__main__":
    cam = open_depth_camera()
    print("Camera opened and started successfully.")
    
    intrinsics = get_intrinsics(cam)
    print("Intrinsics:\n", intrinsics)
    
    extrinsics = get_extrinsics(cam)
    print("Extrinsics:\n", extrinsics)

    depth, confidence = capture_depth_frame(cam)
    print("Captured depth shape:", depth.shape)
    print("Captured confidence shape:", confidence.shape)

    cam.stop()
    cam.close()