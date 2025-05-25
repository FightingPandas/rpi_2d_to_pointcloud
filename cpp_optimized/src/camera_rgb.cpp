// ============================
// 4. camera_rgb.cpp
// ============================
#include "camera_rgb.hpp"

bool RGBCamera::open() {
    std::string pipeline =
        "libcamerasrc ! video/x-raw,width=640,height=480 ! videoconvert ! appsink";

    std::cout << "🔧 Opening with GStreamer pipeline:\n" << pipeline << std::endl;

    if (!cap_.open(pipeline, cv::CAP_GSTREAMER)) {
        std::cerr << "❌ Failed to open RGB camera with libcamera GStreamer pipeline" << std::endl;
        return false;
    }

    std::cout << "✅ Opened RGB camera using libcamera GStreamer pipeline" << std::endl;
    return true;
}

bool RGBCamera::capture(cv::Mat& frame) {
    return cap_.read(frame);
}

void RGBCamera::close() {
    if (cap_.isOpened()) cap_.release();
}