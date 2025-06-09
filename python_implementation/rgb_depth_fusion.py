# rgb_depth_fusion.py
import numpy as np
import open3d as o3d

def fuse_rgb_with_pointcloud(depth_map, rgb_image, K, scale=1000.0):
    h, w = depth_map.shape
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]

    # Compute depth (z) in meters
    z = depth_map.reshape(-1) / scale

    # Generate grid
    i, j = np.meshgrid(np.arange(w), np.arange(h))
    i = i.reshape(-1)
    j = j.reshape(-1)

    # Back-project to 3D
    x = (i - cx) * z / fx
    y = (j - cy) * z / fy

    points = np.stack((x, y, z), axis=-1)  # shape: (N, 3)
    colors = rgb_image.reshape(-1, 3)      # shape: (N, 3)

    valid = np.isfinite(z) & (z > 0)
    return np.hstack((points[valid], colors[valid].astype(np.float32) / 255.0))


def save_colored_pointcloud_ply(points_rgb, filename="pointcloud_rgb.ply"):
    """
    Save a (x, y, z, r, g, b) point cloud to PLY using Open3D.

    Parameters:
        points_rgb (N, 6): numpy array of point cloud with RGB
        filename (str): Output file name
    """
    if points_rgb.shape[1] != 6:
        raise ValueError("Expected point cloud with 6 columns (x, y, z, r, g, b)")

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_rgb[:, :3])
    pcd.colors = o3d.utility.Vector3dVector(points_rgb[:, 3:])
    o3d.io.write_point_cloud(filename, pcd)
    print(f"Saved RGB-D point cloud to {filename}")
