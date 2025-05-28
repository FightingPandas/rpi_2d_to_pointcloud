#include "performance_logger.hpp"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <unistd.h>
#include <sys/resource.h>

PerformanceLogger::PerformanceLogger(const std::string& filename) {
    log_file.open(filename);
    log_file << "Frame,FPS,RGB_Capture_s,Depth_Capture_s,Fusion_s,Memory_MB,CPU_%\n";
    start_time = std::chrono::steady_clock::now();
    last_cpu_check_time = start_time;
    last_cpu_time = 0.0;
}

double PerformanceLogger::getMemoryUsageMB() {
    std::ifstream statm("/proc/self/statm");
    long pages = 0;
    statm >> pages;
    return pages * getpagesize() / (1024.0 * 1024.0);  // Convert to MB
}

double PerformanceLogger::getCPUUtilization() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);

    double current_cpu = usage.ru_utime.tv_sec + usage.ru_utime.tv_usec / 1e6 +
                         usage.ru_stime.tv_sec + usage.ru_stime.tv_usec / 1e6;

    auto now = std::chrono::steady_clock::now();
    double wall_elapsed = std::chrono::duration<double>(now - last_cpu_check_time).count();

    double cpu_util = ((current_cpu - last_cpu_time) / wall_elapsed) * 100.0;

    last_cpu_check_time = now;
    last_cpu_time = current_cpu;

    return cpu_util;
}

void PerformanceLogger::log(int frame, double fps, double t_rgb, double t_depth, double t_fusion) {
    double mem_mb = getMemoryUsageMB();
    double cpu_percent = getCPUUtilization();

    log_file << frame << ","
             << std::fixed << std::setprecision(2)
             << fps << ","
             << std::setprecision(4)
             << t_rgb << ","
             << t_depth << ","
             << t_fusion << ","
             << std::setprecision(2)
             << mem_mb << ","
             << cpu_percent << "\n";

    std::cout << "[LOG] Frame " << frame
              << " | FPS: " << std::fixed << std::setprecision(2) << fps
              << " | RGB: " << std::setprecision(4) << t_rgb << "s"
              << " | Depth: " << t_depth << "s"
              << " | Fusion: " << t_fusion << "s"
              << " | Mem: " << std::setprecision(2) << mem_mb << "MB"
              << " | CPU: " << cpu_percent << "%"
              << std::endl;
}

void PerformanceLogger::close() {
    log_file.close();
}
