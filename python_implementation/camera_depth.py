import ArducamDepthCamera as ac
import numpy as np
from scipy.spatial.transform import Rotation as R
import open3d as o3d

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

def capture_depth_frame(cam, retries=10):
    for attempt in range(retries):
        frame = cam.requestFrame(2000)
        if frame is not None:
            return frame.depth_data, frame.confidence_data
        print(f"⚠️ Retry {attempt + 1}: Failed to capture depth frame")
    raise RuntimeError("Failed to capture frame from depth camera after retries")

def get_intrinsics(cam):
    fx = cam.getControl(ac.Control.INTRINSIC_FX) / 100.0
    fy = cam.getControl(ac.Control.INTRINSIC_FY) / 100.0
    cx = cam.getControl(ac.Control.INTRINSIC_CX) / 100.0
    cy = cam.getControl(ac.Control.INTRINSIC_CY) / 100.0

    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0,  0,  1]])
    return K

def depth_to_pointcloud(depth_map, K, scale=1000.0):
    h, w = depth_map.shape
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]

    i, j = np.meshgrid(np.arange(w), np.arange(h))
    z = depth_map / scale
    x = (i - cx) * z / fx
    y = (j - cy) * z / fy

    points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
    valid = np.isfinite(points[:, 2]) & (points[:, 2] > 0)
    return points[valid]

def save_pointcloud_ply(points, filename="pointcloud.ply"):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(filename, pcd)
    print(f"✅ Saved point cloud to {filename}")

if __name__ == "__main__":
    cam = open_depth_camera()
    print("Camera opened and started successfully.")
    
    intrinsics = get_intrinsics(cam)
    print("Intrinsics:\n", intrinsics)

    depth, confidence = capture_depth_frame(cam)
    print("Captured depth shape:", depth.shape)
    print("Captured confidence shape:", confidence.shape)

    # Generate point cloud
    pointcloud = depth_to_pointcloud(depth, intrinsics)
    print("Generated point cloud with", pointcloud.shape[0], "points.")

    # Save to file
    save_pointcloud_ply(pointcloud)

    cam.stop()
    cam.close()
