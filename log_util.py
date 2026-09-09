# log_util.py
# A homemade logger. Modernised 2025.
# The logging module is preferred for new code; this is kept for compatibility.

import time

LOG_LINES: list[str] = []    # module-level buffer; shared across all importers


def log(message: str) -> None:
    """Append a timestamped line to the buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered lines to path (append mode) and clear the buffer."""
    with open(path, "a", encoding="utf-8") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    del LOG_LINES[:]
