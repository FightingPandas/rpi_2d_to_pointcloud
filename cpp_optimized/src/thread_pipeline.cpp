#include "thread_pipeline.hpp"
#include "camera_depth.hpp"
#include "rgb_depth_fusion.hpp"
#include "ply_writer.hpp"
#include "rgb_reader.hpp"
#include "performance_logger.hpp"  // ✅ NEW

#include <iostream>
#include <opencv2/opencv.hpp>
#include <queue>
#include <thread>
#include <mutex>
#include <atomic>
#include <chrono>

namespace Pipeline {

static std::queue<cv::Mat> depth_queue;
static std::mutex queue_mutex;
static std::atomic<bool> running{false};

static std::thread depth_thread;
static std::thread fusion_thread;

static PerformanceLogger logger("cpp_fusion_log.csv");  // ✅ NEW

void depthCaptureLoop(DepthCamera& cam) {
    while (running) {
        cv::Mat frame;
        if (cam.capture(frame)) {
            std::lock_guard<std::mutex> lock(queue_mutex);
            if (!depth_queue.empty()) depth_queue.pop();  // flush old
            depth_queue.push(frame);
        }
    }
}

void fusionLoop(const cv::Mat K) {
    int frame_index = 0;
    auto prev_time = std::chrono::steady_clock::now();

    while (running) {
        auto start = std::chrono::steady_clock::now();

        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        // DEPTH CAPTURE
        auto t0 = std::chrono::steady_clock::now();
        cv::Mat depth;
        {
            std::lock_guard<std::mutex> lock(queue_mutex);
            if (depth_queue.empty()) continue;
            depth = depth_queue.front();
            depth_queue.pop();
        }
        auto t1 = std::chrono::steady_clock::now();

        // RGB CAPTURE
        cv::Mat rgb = read_rgb_from_shared_memory("psm_1cba8df0", 640, 480);
        if (rgb.empty()) {
            std::cerr << "⚠️ Failed to read RGB from shared memory.\n";
            continue;
        }
        auto t2 = std::chrono::steady_clock::now();

        // GENERATE DEPTH HEATMAP
        cv::Mat depth_display;
        cv::normalize(depth, depth_display, 0, 255, cv::NORM_MINMAX);
        depth_display.convertTo(depth_display, CV_8U);
        cv::applyColorMap(depth_display, depth_display, cv::COLORMAP_JET);

        // Resize RGB if needed
        if (rgb.size() != depth_display.size()) {
            cv::resize(rgb, rgb, depth_display.size());
        }

        // COMPOSITE DISPLAY
        cv::Mat side_by_side;
        cv::hconcat(rgb, depth_display, side_by_side);

        // FPS
        auto now = std::chrono::steady_clock::now();
        double fps = 1.0 / std::chrono::duration<double>(now - prev_time).count();
        prev_time = now;

        // Draw FPS
        cv::putText(side_by_side, "FPS: " + std::to_string(fps).substr(0, 5),
                    cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX,
                    1.0, cv::Scalar(255, 255, 0), 2);

        cv::imshow("RGB | Depth Heatmap", side_by_side);
        if (cv::waitKey(1) == 'q') break;

        auto end = std::chrono::steady_clock::now();

        double t_rgb = std::chrono::duration<double>(t2 - t1).count();
        double t_depth = std::chrono::duration<double>(t1 - t0).count();
        double t_fuse = std::chrono::duration<double>(end - t2).count();
        logger.log(frame_index++, fps, t_rgb, t_depth, t_fuse);

        // Optional: Save point cloud
        // auto cloud = fuseRGBD(depth, rgb, K);
        // savePointCloudPLY(cloud, "/home/kysh/rpi_2d_to_pointcloud/fused_pointclouds/fused_cloud_" + std::to_string(frame_index) + ".ply");
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
    logger.close();  // ✅ NEW
}

}  // namespace Pipeline
