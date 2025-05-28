import open3d as o3d

def visualize_ply(filename="pointcloud_0.ply"):
    print(f"Loading point cloud from {filename}...")
    pcd = o3d.io.read_point_cloud(filename)
    print(f"Loaded point cloud with {len(pcd.points)} points.")

    # Visualize the point cloud
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    
    visualize_ply()
