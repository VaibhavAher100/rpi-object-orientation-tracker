from collections import deque


def update_filter(window: deque, new_angle: float) -> float:
    """
    Add new_angle to the moving average window and return the current average.
    Oldest value is dropped automatically when window is full.
    """
    window.append(new_angle)
    return sum(window) / len(window)


if __name__ == "__main__":
    window = deque(maxlen=5)

    test_angles = [12.3, 13.1, 11.8, 12.5, 13.0, 14.2]

    for angle in test_angles:
        result = update_filter(window, angle)
        print(f"new_angle={angle:.1f}  window={list(window)}  avg={result:.2f}")


# =============================================================================
# PREVIOUS VERSION — kept for reference
# =============================================================================
#
# def make_filter(window_size: int = 5) -> deque:
#     """
#     Create an empty moving average window of fixed maximum size.
#     """
#     return deque(maxlen=window_size)
#
#
# def update_filter(window: deque, new_angle: float) -> float:
#     """
#     Add new_angle to the window and return the current moving average.
#     Oldest value is dropped automatically when window is full.
#     """
#     t_start = time.time()
#
#     window.append(new_angle)
#     avg = sum(window) / len(window)
#
#     t_end = time.time()
#     print(f"update_filter runtime: {t_end - t_start:.6f} seconds")
#
#     return avg
#
# Issues identified:
#   1. make_filter() wraps a single line (deque(maxlen=window_size)) — adds
#      indirection without value. Caller creates the deque directly instead.
#   2. Timing print inside update_filter() runs every frame (~10x per second),
#      spamming the terminal. Per-frame functions must not print runtime.
#      Profiling belongs in a one-time benchmark, not in the hot path.
# =============================================================================
