import numpy as np

def depth_to_pointcloud(depth_map, K, scale=1000.0):
    h, w = depth_map.shape
    fx, fy = K[0][0], K[1][1]
    cx, cy = K[0][2], K[1][2]

    i, j = np.meshgrid(np.arange(w), np.arange(h))
    z = depth_map / scale
    x = (i - cx) * z / fx
    y = (j - cy) * z / fy

    return np.stack((x, y, z), axis=-1)  # shape: (H, W, 3)

def extract_3d_region_from_bbox(pointcloud, bbox):
    # Ensure bbox is a flat list
    bbox = np.array(bbox).flatten()
    x1, y1, x2, y2 = map(int, bbox[:4])
    region = pointcloud[y1:y2, x1:x2, :]
    valid = region[..., 2] > 0
    return region[valid]

def compute_centroid(points):
    return np.mean(points, axis=0) if len(points) > 0 else None
