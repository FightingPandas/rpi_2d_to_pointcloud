from camera_rgb import open_rgb_camera, capture_rgb_frame
from camera_depth import open_depth_camera, capture_depth_frame, get_intrinsics
from detection import Detector
from fusion import depth_to_pointcloud, extract_3d_region_from_bbox, compute_centroid
from visualize import show_overlay, visualize_pointcloud_3d
import numpy as np
import cv2

def main():
    rgb_cam = open_rgb_camera()
    depth_cam = open_depth_camera()
    intrinsics = get_intrinsics(depth_cam)
    detector = Detector("model.tflite")

    while True:
        rgb = capture_rgb_frame(rgb_cam)
        depth, _ = capture_depth_frame(depth_cam)
        boxes = detector.detect(rgb)

        pointcloud = depth_to_pointcloud(depth, intrinsics)
        depths = []

        for box in boxes:
            region_points = extract_3d_region_from_bbox(pointcloud, box)
            centroid = compute_centroid(region_points)
            depths.append(centroid[2] if centroid is not None else 0)

        show_overlay(rgb.copy(), boxes, depths)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('v'):
            visualize_pointcloud_3d(pointcloud)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
