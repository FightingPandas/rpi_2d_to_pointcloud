// rgb_depth_fusion.cpp
#include "rgb_depth_fusion.hpp"
#include <cmath>

std::vector<cv::Vec6f> fuseRGBD(const cv::Mat& depth_map, const cv::Mat& rgb_image, const cv::Mat& K, float scale) {
    std::vector<cv::Vec6f> fused;
    int h = depth_map.rows;
    int w = depth_map.cols;

    float fx = K.at<float>(0, 0);
    float fy = K.at<float>(1, 1);
    float cx = K.at<float>(0, 2);
    float cy = K.at<float>(1, 2);

    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            float d = depth_map.at<float>(y, x);
            if (!std::isfinite(d) || d <= 0.0f) continue;

            float Z = d / scale;
            float X = (x - cx) * Z / fx;
            float Y = (y - cy) * Z / fy;

            cv::Vec3b color = rgb_image.at<cv::Vec3b>(y, x);
            fused.emplace_back(X, Y, Z,
                               color[2] / 255.0f,  // R
                               color[1] / 255.0f,  // G
                               color[0] / 255.0f); // B
        }
    }
    return fused;
}
