// ply_writer.cpp
#include "ply_writer.hpp"
#include <fstream>
#include <iomanip>

bool savePointCloudPLY(const std::vector<cv::Vec6f>& cloud, const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) return false;

    file << "ply\nformat ascii 1.0\nelement vertex " << cloud.size() << "\n";
    file << "property float x\nproperty float y\nproperty float z\n";
    file << "property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n";

    for (const auto& pt : cloud) {
        file << pt[0] << " " << pt[1] << " " << pt[2] << " "
             << static_cast<int>(pt[3] * 255) << " "
             << static_cast<int>(pt[4] * 255) << " "
             << static_cast<int>(pt[5] * 255) << "\n";
    }

    return true;
}
