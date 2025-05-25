#include "thread_pipeline.hpp"
#include "camera_depth.hpp"
#include "rgb_depth_fusion.hpp"
#include "ply_writer.hpp"
#include "rgb_reader.hpp"  // ✅ NEW

#include <iostream>
#include <opencv2/opencv.hpp>
#include <queue>
#include <thread>
#include <mutex>
#include <atomic>

namespace Pipeline {

static std::queue<cv::Mat> depth_queue;
static std::mutex queue_mutex;
static std::atomic<bool> running{false};

static std::thread depth_thread;
static std::thread fusion_thread;

void depthCaptureLoop(DepthCamera& cam) {
    while (running) {
        cv::Mat frame;
        if (cam.capture(frame)) {
            std::lock_guard<std::mutex> lock(queue_mutex);
            depth_queue.push(frame);
        }
    }
}

void fusionLoop(const cv::Mat K) {
    int frame_index = 0;
    while (running) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        cv::Mat depth;
        {
            std::lock_guard<std::mutex> lock(queue_mutex);
            if (depth_queue.empty()) continue;
            depth = depth_queue.front();
            depth_queue.pop();
        }

        // ✅ Read RGB directly from shared memory
        cv::Mat rgb = read_rgb_from_shared_memory("psm_1cba8df0", 640, 480);
        if (rgb.empty()) {
            std::cerr << "⚠️ Failed to read RGB from shared memory.\n";
            continue;
        }

        auto cloud = fuseRGBD(depth, rgb, K);
        savePointCloudPLY(cloud, "fused_cloud_" + std::to_string(frame_index++) + ".ply");
    }
}

void start(DepthCamera& depthCam, const cv::Mat& K) {
    running = true;
    depth_thread = std::thread(depthCaptureLoop, std::ref(depthCam));
    fusion_thread = std::thread(fusionLoop, K);
}

void stop() {
    running = false;
    if (depth_thread.joinable()) depth_thread.join();
    if (fusion_thread.joinable()) fusion_thread.join();
}

}  // namespace Pipeline
