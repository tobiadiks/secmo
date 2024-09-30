import os

# Fetch and filter logs
def fetch_filtered_logs(log_file_path, include_levels=None, max_lines=100):
    """
    Reads and filters the log file from the given path based on log levels.
    Only includes the specified log levels (e.g., ERROR, WARNING).
    """
    if not include_levels:
        include_levels = ['ERROR', 'WARNING']  # Default log levels to focus on

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            filtered_logs = []
            for line in log_file:
                # Check if the log line contains the desired log levels
                if any(level in line for level in include_levels):
                    filtered_logs.append(line)
                if len(filtered_logs) >= max_lines:
                    break  # Stop after max_lines to limit tokens usage
            return ''.join(filtered_logs)  # Return the filtered logs as a string
    else:
        raise FileNotFoundError(f"Log file not found at {log_file_path}")