import cv2
import open3d as o3d
import numpy as np

def show_overlay(rgb, boxes, depths):
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"Z: {depths[i]:.2f}m"
        cv2.putText(rgb, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.imshow("Overlay", rgb)

def visualize_pointcloud_3d(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points.reshape(-1, 3))
    o3d.visualization.draw_geometries([pcd])
