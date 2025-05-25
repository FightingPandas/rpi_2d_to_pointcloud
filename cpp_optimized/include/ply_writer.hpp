// ply_writer.hpp
#pragma once

#include <opencv2/core.hpp>
#include <string>
#include <vector>

// Writes point cloud in ASCII PLY format
bool savePointCloudPLY(const std::vector<cv::Vec6f>& cloud, const std::string& filename);
