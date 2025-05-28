#pragma once
#include <fstream>
#include <chrono>
#include <string>

class PerformanceLogger {
public:
    PerformanceLogger(const std::string& filename);
    void log(int frame, double fps, double t_rgb, double t_depth, double t_fusion);
    void close();

private:
    std::ofstream log_file;
    std::chrono::steady_clock::time_point start_time;
    std::chrono::steady_clock::time_point last_cpu_check_time;  // NEW
    double last_cpu_time;  // NEW

    double getMemoryUsageMB();
    double getCPUUtilization();  // NEW
};
