#!/bin/bash

echo "🚀 Launching RGB writer (Python)..."
python3 python_rgb/rgb_writer.py &
PY_PID=$!

echo "🧠 Waiting for camera warm-up..."
sleep 2

echo "🛠️  Launching fusion pipeline (main.cpp)..."
./cpp_optimized/build/rgbd_fusion

echo "🧹 Shutting down RGB writer..."
kill $PY_PID
