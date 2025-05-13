import psutil
import time
import csv

class PerformanceLogger:
    def __init__(self, filename="performance_log.csv"):
        self.process = psutil.Process()
        self.start_time = time.time()
        self.fps_list = []
        self.frame_count = 0
        self.csvfile = open(filename, "w", newline='')
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow(["Frame", "FPS", "CPU (%)", "Memory (MB)", "RGB Capture (s)", "Depth Capture (s)", "Fusion (s)"])

    def log(self, frame_number, fps, t_rgb, t_depth, t_fusion):
        cpu_usage = self.process.cpu_percent(interval=0)  # Non-blocking snapshot
        mem_usage = self.process.memory_info().rss / (1024 * 1024)  # MB

        self.writer.writerow([frame_number, fps, cpu_usage, mem_usage, t_rgb, t_depth, t_fusion])
        print(f"[INFO] Frame {frame_number}: FPS {fps:.2f} | CPU {cpu_usage:.1f}% | Mem {mem_usage:.1f} MB | RGB {t_rgb:.3f}s | Depth {t_depth:.3f}s | Fusion {t_fusion:.3f}s")

    def close(self):
        self.csvfile.close()
