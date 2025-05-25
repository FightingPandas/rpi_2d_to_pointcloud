// rgb_depth_fusion.hpp
#pragma once

#include <opencv2/core.hpp>
#include <vector>

// Each point: x, y, z, r, g, b
std::vector<cv::Vec6f> fuseRGBD(const cv::Mat& depth_map, const cv::Mat& rgb_image, const cv::Mat& K, float scale = 1000.0f);
