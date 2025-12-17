import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def analyze_trajectory(file_path):
    print(f"Analyzing {file_path}...")
    
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) < 8:
                continue
            # Format: timestamp(s) qx qy qz qw px py pz ...
            # Index:  0            1  2  3  4  5  6  7
            ts = float(parts[0])
            px = float(parts[5])
            py = float(parts[6])
            pz = float(parts[7])
            data.append([ts, px, py, pz])
            
    data = np.array(data)
    
    if len(data) == 0:
        print("Error: No data found in file.")
        return

    # 1. Calculate Start-to-End Error
    start_pos = data[0, 1:4]
    end_pos = data[-1, 1:4]
    error_vec = end_pos - start_pos
    error_norm = np.linalg.norm(error_vec)
    
    # 2. Calculate Path Length
    diffs = np.diff(data[:, 1:4], axis=0)
    dists = np.linalg.norm(diffs, axis=1)
    path_length = np.sum(dists)
    
    # 3. Calculate Drift Percentage
    drift_percentage = (error_norm / path_length) * 100 if path_length > 0 else 0
    
    print("="*40)
    print("SLAM Evaluation Results")
    print("="*40)
    print(f"Total Duration: {data[-1, 0] - data[0, 0]:.2f} s")
    print(f"Path Length:    {path_length:.3f} m")
    print(f"Start Position: {start_pos}")
    print(f"End Position:   {end_pos}")
    print("-" * 40)
    print(f"Start-to-End Error (Drift): {error_norm:.4f} m")
    print(f"Drift Percentage:           {drift_percentage:.2f}%")
    print("="*40)
    
    # 4. Plot Trajectory (X-Y)
    plt.figure(figsize=(10, 8))
    plt.plot(data[:, 1], data[:, 2], label='Trajectory', linewidth=1)
    plt.scatter([start_pos[0]], [start_pos[1]], color='green', marker='o', s=100, label='Start')
    plt.scatter([end_pos[0]], [end_pos[1]], color='red', marker='x', s=100, label='End')
    plt.title(f"SLAM Trajectory (X-Y)\nDrift: {error_norm:.3f}m ({drift_percentage:.2f}%)")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    
    output_img = file_path.replace('.txt', '_plot.png')
    plt.savefig(output_img)
    print(f"Trajectory plot saved to: {output_img}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_results.py <path_to_state_estimate.txt>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
        
    analyze_trajectory(file_path)
