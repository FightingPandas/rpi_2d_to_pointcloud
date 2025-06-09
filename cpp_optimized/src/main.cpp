#include "camera_depth.hpp"
#include "thread_pipeline.hpp"
#include "rgb_reader.hpp"  

#include <iostream>

int main() {
    DepthCamera depthCam;

    std::cout << "Opening depth camera...\n";
    if (!depthCam.open() || !depthCam.start()) {
        std::cerr << "Failed to initialize depth camera.\n";
        return -1;
    }

    cv::Mat K = depthCam.getIntrinsicsMatrix();

    std::cout << "Starting threaded RGB-D fusion pipeline...\n";
    Pipeline::start(depthCam, K); 

    std::cout << "Running... press ENTER to stop.\n";
    std::cin.get();  // Wait for user to press enter

    std::cout << "Stopping pipeline...\n";
    Pipeline::stop();
    depthCam.stop();
    depthCam.close();

    std::cout << "Done.\n";
    return 0;
}
