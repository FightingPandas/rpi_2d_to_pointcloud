// ============================
// 3. camera_rgb.hpp
// ============================
#pragma once
#include <opencv2/opencv.hpp>

class RGBCamera {
public:
    bool open();
    bool capture(cv::Mat& frame);
    void close();

private:
    cv::VideoCapture cap_;
};