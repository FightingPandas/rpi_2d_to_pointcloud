// thread_pipeline.hpp
#pragma once

#include <opencv2/core.hpp>
#include <queue>
#include <mutex>
#include <atomic>
#include <thread>
#include <condition_variable>

class DepthCamera;
class RGBCamera;

namespace Pipeline {

void start(DepthCamera& depthCam, const cv::Mat& K);
void stop();

}  // namespace Pipeline
