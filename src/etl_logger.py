# src/etl_logger.py
import csv, os
from datetime import datetime

LOG_FILE = "data/etl_log.csv"

def log_event(process, message, status):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "process", "message", "status"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), process, message, status])

if __name__ == "__main__":
    log_event("logger_test", "Logger initialized successfully", "SUCCESS")
