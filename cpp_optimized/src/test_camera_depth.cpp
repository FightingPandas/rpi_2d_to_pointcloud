#include "camera_depth.hpp"
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

int main() {
    DepthCamera depth_cam;

    if (!depth_cam.open()) {
        std::cerr << "❌ Failed to open depth camera\n";
        return -1;
    }

    if (!depth_cam.start()) {
        std::cerr << "❌ Failed to start depth stream\n";
        return -1;
    }

    cv::Mat frame;
    if (depth_cam.capture(frame)) {
        std::cout << "✅ Captured depth frame: " << frame.cols << "x" << frame.rows << "\n";

        // Visualize depth
        cv::Mat vis;
        cv::normalize(frame, vis, 0, 255, cv::NORM_MINMAX);
        vis.convertTo(vis, CV_8U);
        cv::applyColorMap(vis, vis, cv::COLORMAP_JET);
        cv::imshow("Depth Frame", vis);
        cv::waitKey(0);
    } else {
        std::cerr << "⚠️ Failed to capture depth frame\n";
    }

    cv::Mat K = depth_cam.getIntrinsicsMatrix();
    std::cout << "Camera intrinsics:\n" << K << "\n";

    depth_cam.stop();
    depth_cam.close();
    return 0;
}
