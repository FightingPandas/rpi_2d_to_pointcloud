#include "camera_rgb.hpp"
#include <opencv2/highgui.hpp>
#include <iostream>

int main() {
    std::cout << "🚀 test_camera_rgb is running\n";

    RGBCamera rgb_cam;
    std::cout << "🟡 Attempting to open RGB camera...\n";

    if (!rgb_cam.open()) {
        std::cerr << "❌ Failed to open RGB camera\n";
        return -1;
    }

    std::cout << "✅ RGB camera opened successfully\n";

    cv::Mat frame;
    std::cout << "🟡 Capturing frame...\n";

    if (rgb_cam.capture(frame)) {
        std::cout << "✅ Captured RGB frame: " << frame.cols << "x" << frame.rows << "\n";
        cv::imwrite("rgb_frame.jpg", frame);
        std::cout << "🖼 Saved frame as rgb_frame.jpg\n";
        // cv::imshow("RGB Frame", frame);  // Commented out for headless use
        // cv::waitKey(0);
    } else {
        std::cerr << "⚠️ Failed to capture RGB frame\n";
    }

    rgb_cam.close();
    return 0;
}

