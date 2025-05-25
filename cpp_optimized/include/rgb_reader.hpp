// rgb_reader.hpp
#pragma once
#include <opencv2/opencv.hpp>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

inline cv::Mat read_rgb_from_shared_memory(const char* shm_name, int width, int height) {
    int size = width * height * 3;
    int fd = shm_open(shm_name, O_RDONLY, 0666);
    if (fd == -1) {
        perror("shm_open");
        return {};
    }

    void* ptr = mmap(NULL, size, PROT_READ, MAP_SHARED, fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return {};
    }

    cv::Mat rgb(height, width, CV_8UC3, ptr);
    cv::Mat cloned = rgb.clone();  // Clone to own memory
    munmap(ptr, size);
    close(fd);
    return cloned;
}
