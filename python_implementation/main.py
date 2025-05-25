import cv2
import numpy as np
import time
from camera_rgb import open_rgb_camera, capture_rgb_frame
from camera_depth import open_depth_camera, capture_depth_frame, get_intrinsics
from performance_logger import PerformanceLogger  # Import logger
from rgb_depth_fusion import fuse_rgb_with_pointcloud, save_colored_pointcloud_ply
import open3d as o3d  # Still used for display fallback

def main():
    logger = PerformanceLogger("main_baseline_log.csv")

    print("Initializing cameras...")
    depth_cam = open_depth_camera()
    rgb_cam = open_rgb_camera()
    K = get_intrinsics(depth_cam)

    print("Starting main fusion loop...")
    prev_time = time.time()
    frame_count = 0

    while True:
        t0 = time.time()
        rgb_frame = capture_rgb_frame(rgb_cam)
        if rgb_frame.shape[-1] > 3:
            rgb_frame = rgb_frame[..., :3]
        t1 = time.time()

        frame = depth_cam.requestFrame(2000)
        if frame is None:
            print("⚠️ Depth frame failed, skipping...")
            continue
        depth_frame = frame.depth_data
        t2 = time.time()

        # Resize depth to match RGB resolution
        depth_resized = cv2.resize(depth_frame, (rgb_frame.shape[1], rgb_frame.shape[0]), interpolation=cv2.INTER_NEAREST)
        t3 = time.time()

        # Generate and save RGB-D fused point cloud every N frames
        if frame_count % 50 == 0:
            print("Depth shape:", depth_resized.shape)
            print("RGB shape:", rgb_frame.shape)
            fused_cloud = fuse_rgb_with_pointcloud(depth_resized, rgb_frame, K)
            print(f"Generated RGB-D point cloud with {fused_cloud.shape[0]} points.")
            save_colored_pointcloud_ply(fused_cloud, filename=f"fused_pointcloud_{frame_count}.ply")

        # Create a depth heatmap for display
        depth_norm = cv2.normalize(depth_resized, None, 0, 255, cv2.NORM_MINMAX)
        depth_colored = cv2.applyColorMap(depth_norm.astype(np.uint8), cv2.COLORMAP_JET)

        # Side-by-side display
        display = np.hstack((rgb_frame[:, :, :3], depth_colored))

        # FPS overlay
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(display, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Log performance
        logger.log(frame_count, fps, t1 - t0, t2 - t1, t3 - t2)

        cv2.imshow("RGB | Depth Heatmap", display)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        frame_count += 1

    print("Stopping cameras...")
    logger.close()
    cv2.destroyAllWindows()
    depth_cam.stop()
    depth_cam.close()

if __name__ == "__main__":
    main()
