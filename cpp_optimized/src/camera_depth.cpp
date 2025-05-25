// camera_depth.cpp
#include "camera_depth.hpp"
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

#define MAX_DISTANCE 4000

DepthCamera::DepthCamera() : opened_(false) {}

bool DepthCamera::open() {
    if (cam_.open(Arducam::Connection::CSI, 8) != 0) {
        std::cerr << "❌ Failed to open Arducam Depth Camera.\n";
        return false;
    }
    cam_.setControl(Arducam::Control::RANGE, MAX_DISTANCE);
    opened_ = true;
    return true;
}

bool DepthCamera::start() {
    return opened_ && cam_.start(Arducam::FrameType::DEPTH_FRAME) == 0;
}

bool DepthCamera::stop() {
    return opened_ && cam_.stop() == 0;
}

bool DepthCamera::close() {
    return opened_ && cam_.close() == 0;
}

bool DepthCamera::capture(cv::Mat& depth_map) {
    if (!opened_) return false;
    Arducam::ArducamFrameBuffer* frame = cam_.requestFrame(2000);
    if (!frame) return false;

    Arducam::FrameFormat format;
    frame->getFormat(Arducam::FrameType::DEPTH_FRAME, format);
    int width = format.width;
    int height = format.height;

    float* data = (float*)frame->getData(Arducam::FrameType::DEPTH_FRAME);
    depth_map = cv::Mat(height, width, CV_32F, data).clone();

    cam_.releaseFrame(frame);
    return true;
}

cv::Mat DepthCamera::getIntrinsicsMatrix() {
    int fx_raw, fy_raw, cx_raw, cy_raw;
    cam_.getControl(Arducam::Control::INTRINSIC_FX, &fx_raw);
    cam_.getControl(Arducam::Control::INTRINSIC_FY, &fy_raw);
    cam_.getControl(Arducam::Control::INTRINSIC_CX, &cx_raw);
    cam_.getControl(Arducam::Control::INTRINSIC_CY, &cy_raw);

    float fx = fx_raw / 100.0f;
    float fy = fy_raw / 100.0f;
    float cx = cx_raw / 100.0f;
    float cy = cy_raw / 100.0f;

    return (cv::Mat_<float>(3, 3) << fx, 0, cx,
                                    0, fy, cy,
                                    0,  0,  1);
}
