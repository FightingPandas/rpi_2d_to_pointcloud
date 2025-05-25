#pragma once
#include <opencv2/core.hpp>
#include <ArducamTOFCamera.hpp>

class DepthCamera {
public:
    DepthCamera();
    bool open();
    bool start();
    bool stop();
    bool close();
    bool capture(cv::Mat& depth_frame);
    cv::Mat getIntrinsicsMatrix();

private:
    Arducam::ArducamTOFCamera cam_;
    bool opened_;
};
