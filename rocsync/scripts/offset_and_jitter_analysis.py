import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

def load_inliers(inlier_path):
    with open(inlier_path, 'r') as f:
        inlier_ms = json.load(f)
    return set(inlier_ms)

def load_filtered_timestamps(full_json_path, inlier_timestamps_ms):
    with open(full_json_path, 'r') as f:
        data = json.load(f)

    ros_ts_ns = []
    led_ts_ns = []

    for fname, val in data.items():
        match = re.search(r'_(\d+)_(\d+)\.png$', Path(fname).name)
        if not match:
            continue

        ros_sec = int(match.group(1))
        ros_nsec = int(match.group(2))
        ros_ns = ros_sec * 10**9 + ros_nsec

        led_ms_lo = val.get("start", None)
        if led_ms_lo is None or led_ms_lo not in inlier_timestamps_ms:
            continue
        led_ms_hi = val.get("end", None)
        if led_ms_hi is None:
            continue

        # led_ms = (led_ms_lo + led_ms_hi) / 2
        led_ms = led_ms_lo  # Use start time for consistency

        ros_ts_ns.append(ros_ns)
        led_ts_ns.append(led_ms * 10**6)

    return np.array(ros_ts_ns), np.array(led_ts_ns)

def reject_offset_outliers(offsets_ns, threshold_ns=5_000_000):  # ±5ms by default
    median = np.median(offsets_ns)
    diffs = np.abs(offsets_ns - median)
    mask = diffs < threshold_ns
    return mask

def analyze_camera(name, ros_ts, led_ts, threshold_ns=5_000_000):
    offsets = ros_ts - led_ts
    mask = reject_offset_outliers(offsets, threshold_ns)
    filtered_offsets = offsets[mask]
    filtered_ros = ros_ts[mask]
    filtered_led = led_ts[mask]

    mean = np.mean(filtered_offsets)
    stddev = np.std(filtered_offsets)

    print(f"\n📷 {name} camera:")
    print(f"  Frame count (original): {len(offsets)}")
    print(f"  Frame count (after outlier rejection): {len(filtered_offsets)}")
    print(f"  Offset mean: {mean:.0f} ns ({mean/1e6:.3f} ms)")
    print(f"  Offset stddev (jitter): {stddev:.0f} ns ({stddev/1e6:.3f} ms)")

    plt.figure(figsize=(10, 4))
    # plt.plot(ros_ts / 1e9, offsets / 1e6, '.', alpha=0.2, label="All")
    plt.plot(filtered_ros / 1e9, filtered_offsets / 1e6, '.', alpha=0.7, label="Filtered")
    plt.xlabel("ROS time [s]")
    plt.ylabel("Offset (ROS - LED) [ms]")
    plt.title(f"{name} Offset Over Time")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 4))
    plt.hist((filtered_offsets - mean) / 1e6, bins=60, color='steelblue', edgecolor='black')
    plt.xlabel("Offset [ms]")
    plt.ylabel("Count")
    plt.title(f"{name} Offset Distribution (Filtered)")
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    # oak_raw = "/home/fred/Downloads/oak_timestamps.json"
    # oak_rgb_raw = "/home/fred/Downloads/oak_timestamps_rgb.json"
    fusion_raw = "/home/fred/Downloads/atracsys_timestamps.json"
    # oak_inliers = "/home/fred/Downloads/oak_inliers.json"
    # oak_rgb_inliers = "/home/fred/Downloads/oak_rgb_inliers.json"
    fusion_inliers = "/home/fred/Downloads/atracsys_inliers.json"

    # oak_ros, oak_led = load_filtered_timestamps(oak_raw, load_inliers(oak_inliers))
    # oak_rgb_ros, oak_rgb_led = load_filtered_timestamps(oak_rgb_raw, load_inliers(oak_rgb_inliers))
    fusion_ros, fusion_led = load_filtered_timestamps(fusion_raw, load_inliers(fusion_inliers))

    # analyze_camera("OAK", oak_ros, oak_led)
    # analyze_camera("OAK RGB", oak_rgb_ros, oak_rgb_led)
    analyze_camera("Fusion", fusion_ros, fusion_led)


if __name__ == "__main__":
    main()
