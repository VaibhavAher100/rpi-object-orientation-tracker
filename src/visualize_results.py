import csv
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "results", "detections.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "results", "angle_trace.png")


def load_results(filepath: str) -> tuple:
    """
    Read detections CSV and return four lists:
    timestamps, raw_angles, filtered_angles, object_counts.
    """
    timestamps, raw_angles, filtered_angles, object_counts = [], [], [], []

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(float(row["timestamp"]))
            raw_angles.append(float(row["raw_angle"]))
            filtered_angles.append(float(row["filtered_angle"]))
            object_counts.append(int(row["object_count"]))

    # normalise timestamps to start at 0
    t0 = timestamps[0]
    timestamps = [t - t0 for t in timestamps]

    return timestamps, raw_angles, filtered_angles, object_counts


def plot_results(timestamps: list, raw_angles: list, filtered_angles: list, object_counts: list) -> None:
    """
    Plot raw angle, filtered angle, and object count as three stacked subplots.
    Saves output to results/angle_trace.png.
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))
    fig.suptitle("Object Orientation Tracker — Detection Results")

    axes[0].plot(timestamps, raw_angles, color="steelblue", linewidth=0.8)
    axes[0].set_ylabel("Raw Angle (°)")
    axes[0].set_ylim(-5, 185)
    axes[0].grid(True)

    axes[1].plot(timestamps, filtered_angles,
                 color="darkorange", linewidth=0.8)
    axes[1].set_ylabel("Filtered Angle (°)")
    axes[1].set_ylim(-5, 185)
    axes[1].grid(True)

    axes[2].plot(timestamps, object_counts, color="green", linewidth=0.8)
    axes[2].set_ylabel("Object Count")
    axes[2].set_xlabel("Time (seconds)")
    axes[2].set_ylim(-0.5, 3)
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=150)
    print(f"saved {OUTPUT_FILE}")


if __name__ == "__main__":
    timestamps, raw_angles, filtered_angles, object_counts = load_results(
        LOG_FILE)
    plot_results(timestamps, raw_angles, filtered_angles, object_counts)
