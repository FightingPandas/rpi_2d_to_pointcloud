cmake_minimum_required(VERSION 3.10)
project(rgbd_fusion)

set(CMAKE_CXX_STANDARD 17)

include_directories(
    ${CMAKE_SOURCE_DIR}/include
    /usr/include/opencv4
)

link_directories(/usr/lib)

find_package(OpenCV REQUIRED)

# Main executable: C++ fusion pipeline
add_executable(rgbd_fusion
    src/main.cpp
    src/performance_logger.cpp
    src/camera_depth.cpp
    src/ply_writer.cpp
    src/rgb_depth_fusion.cpp
    src/thread_pipeline.cpp
)
target_link_libraries(rgbd_fusion ${OpenCV_LIBS} ArducamDepthCamera)

# Test executables (optional, keep if still needed)
# add_executable(test_camera_depth src/test_camera_depth.cpp src/camera_depth.cpp)
# target_include_directories(test_camera_depth PRIVATE include)
# target_link_libraries(test_camera_depth ${OpenCV_LIBS} ArducamDepthCamera)

# Optionally remove this if you're no longer using camera_rgb
# add_executable(test_camera_rgb src/test_camera_rgb.cpp src/camera_rgb.cpp)
# target_include_directories(test_camera_rgb PRIVATE include)
# target_link_libraries(test_camera_rgb ${OpenCV_LIBS})
