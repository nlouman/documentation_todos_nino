import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_rocsync_starts(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    timestamps = []
    for fname, ts in data.items():
        if "start" in ts:
            timestamps.append(ts["start"])
    return timestamps

def reject_outliers_by_gradient(timestamps, tolerance=50, min_chain=5, min_abs_grad=1):
    timestamps = np.array(timestamps)
    diffs = np.diff(timestamps)
    grad_med = np.median(diffs)

    n = len(timestamps)
    inliers = np.zeros(n, dtype=bool)

    for i in range(n):
        forward = 0
        for j in range(i, min(i + min_chain, n - 1)):
            step = timestamps[j + 1] - timestamps[j]
            if abs(step) < min_abs_grad:
                break  # too flat
            if abs(step - grad_med) < tolerance:
                forward += 1
            else:
                break

        backward = 0
        for j in range(i, max(i - min_chain, 0), -1):
            step = timestamps[j] - timestamps[j - 1]
            if abs(step) < min_abs_grad:
                break
            if abs(step - grad_med) < tolerance:
                backward += 1
            else:
                break

        if forward >= min_chain - 1 or backward >= min_chain - 1:
            inliers[i] = True

    return inliers


def reject_outliers(timestamps, window_size=21, threshold=50):
    timestamps = np.array(timestamps)
    n = len(timestamps)
    inliers = np.ones(n, dtype=bool)

    half_window = window_size // 2

    for i in range(n):
        start = max(0, i - half_window)
        end = min(n, i + half_window + 1)
        local = np.concatenate((timestamps[start:i], timestamps[i+1:end]))

        if len(local) == 0:
            continue

        local_median = np.median(local)
        if abs(timestamps[i] - local_median) > threshold:
            inliers[i] = False

    return inliers


def plot_diffs(timestamps, inlier_mask, title):
    diffs = np.diff(timestamps)
    inlier_diffs = np.array(diffs)[inlier_mask[1:]]
    outlier_diffs = np.array(diffs)[~inlier_mask[1:]]

    plt.figure(figsize=(12, 5))
    plt.plot(diffs, label='All frame intervals', color='gray', alpha=0.5)
    plt.plot(np.where(inlier_mask[1:])[0], inlier_diffs, 'g.', label='Inliers')
    plt.plot(np.where(~inlier_mask[1:])[0], outlier_diffs, 'r.', label='Outliers')
    plt.xlabel("Frame index")
    plt.ylabel("Interval (ms)")
    plt.title(f"{title} Frame Interval Analysis")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_timestamps(timestamps, inlier_mask, title):
    timestamps = np.array(timestamps)
    x = np.arange(len(timestamps))
    inlier_x = x[inlier_mask]
    inlier_y = timestamps[inlier_mask]
    outlier_x = x[~inlier_mask]
    outlier_y = timestamps[~inlier_mask]

    # Clamp y-axis to show the main spread (e.g., 1st to 99th percentile of inliers)
    if len(inlier_y) > 0:
        lower = np.percentile(inlier_y, 0.1)
        upper = np.percentile(inlier_y, 99.9)
    else:
        lower, upper = np.min(timestamps), np.max(timestamps)

    plt.figure(figsize=(12, 5))
    plt.plot(x, timestamps, color='gray', alpha=0.5, label='All timestamps')
    plt.scatter(inlier_x, inlier_y, color='green', label='Inliers')
    plt.scatter(outlier_x, outlier_y, color='red', label='Outliers')
    plt.xlabel("Timestamp number")
    plt.ylabel("Timestamp (ms)")
    plt.title(f"{title} Timestamps")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.ylim(lower, upper)
    plt.show()

def print_stats(name, timestamps, inlier_mask):
    inlier_ts = np.array(timestamps)[inlier_mask]
    diffs = np.diff(inlier_ts)
    print(f"\n📷 {name} stats:")
    print(f"  Total frames: {len(timestamps)}")
    print(f"  Inlier frames: {np.sum(inlier_mask)}")
    print(f"  Mean interval: {np.mean(diffs):.2f} ms")
    print(f"  Jitter (std): {np.std(diffs):.2f} ms")
    print(f"  First timestamp: {inlier_ts[0]} ms")

def main():
    # oak_path = "/home/fred/Downloads/oak_timestamps.json"
    # oak_rgb_path = "/home/fred/Downloads/oak_timestamps_rgb.json"
    fusion_path = "/home/fred/Downloads/atracsys_timestamps.json"

    # oak_timestamps = load_rocsync_starts(oak_path)
    # oak_rgb_timestamps = load_rocsync_starts(oak_rgb_path)
    fusion_timestamps = load_rocsync_starts(fusion_path)

    # oak_inliers = reject_outliers(oak_timestamps)
    # oak_rgb_inliers = reject_outliers(oak_rgb_timestamps)
    fusion_inliers = reject_outliers_by_gradient(fusion_timestamps)

    # Save inlier timestamps to new files
    # oak_inlier_timestamps = np.array(oak_timestamps)[oak_inliers].tolist()
    # oak_rgb_inlier_timestamps = np.array(oak_rgb_timestamps)[oak_rgb_inliers].tolist()
    fusion_inlier_timestamps = np.array(fusion_timestamps)[fusion_inliers].tolist()

    # with open("/home/fred/Downloads/oak_inliers.json", "w") as f:
    #     json.dump(oak_inlier_timestamps, f, indent=2)
    # with open("/home/fred/Downloads/oak_rgb_inliers.json", "w") as f:
    #     json.dump(oak_rgb_inlier_timestamps, f, indent=2)
    with open("/home/fred/Downloads/atracsys_inliers.json", "w") as f:
        json.dump(fusion_inlier_timestamps, f, indent=2)

    # plot_diffs(oak_timestamps, oak_inliers, "OAK Camera")
    # plot_diffs(oak_rgb_timestamps, oak_rgb_inliers, "OAK RGB Camera")
    plot_diffs(fusion_timestamps, fusion_inliers, "Fusion Camera")

    # plot_timestamps(oak_timestamps, oak_inliers, "OAK Camera")
    # plot_timestamps(oak_rgb_timestamps, oak_rgb_inliers, "OAK RGB Camera")
    plot_timestamps(fusion_timestamps, fusion_inliers, "Fusion Camera")

    # print_stats("OAK", oak_timestamps, oak_inliers)
    # print_stats("OAK RGB", oak_rgb_timestamps, oak_rgb_inliers)
    print_stats("Fusion", fusion_timestamps, fusion_inliers)

if __name__ == "__main__":
    main()
