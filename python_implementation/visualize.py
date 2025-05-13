import cv2
import open3d as o3d
import numpy as np

def show_overlay(rgb):
    # Simply show the RGB frame with an overlay label (no boxes)
    overlay = rgb.copy()
    cv2.putText(overlay, "Fusion Mode: RGB + Depth (No Detection)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Fusion Overlay", overlay)

def visualize_pointcloud_3d(points):
    # Assumes points is (H, W, 3) or (N, 3)
    if points.ndim == 3:
        points = points.reshape(-1, 3)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])
