import json, os
from datetime import datetime

DATA_PATH = "data"
summary_file = os.path.join(DATA_PATH, "etl_summary.json")

if os.path.exists(summary_file):
    with open(summary_file) as f:
        summary = json.load(f)
    print("Last ETL Summary:")
    for k,v in summary.items():
        print(f"{k:15}: {v}")
else:
    print("No summary file found. Run ETL first.")
