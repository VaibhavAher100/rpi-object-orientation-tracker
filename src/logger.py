import csv
import time
import os


def log_result(
    filepath: str,
    timestamp: float,
    raw_angle: float,
    filtered_angle: float,
    object_count: int,
) -> None:
    """
    Append one row of detection results to a CSV file.
    Creates the file and any missing parent directories if they do not exist yet.
    """

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file_exists = os.path.isfile(filepath)

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                ["timestamp", "raw_angle", "filtered_angle", "object_count"]
            )

        writer.writerow([timestamp, raw_angle, filtered_angle, object_count])


if __name__ == "__main__":
    test_log = "test_results.csv"

    log_result(test_log, time.time(), 12.3, 12.30, 1)
    log_result(test_log, time.time(), 13.1, 12.70, 1)
    log_result(test_log, time.time(), 11.8, 12.40, 1)

    print("written to", test_log)
