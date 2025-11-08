import pandas as pd
import sqlite3, os, json
from datetime import datetime

DATA_PATH = "data"
DB_PATH = os.path.join(DATA_PATH, "reminder_system.db")
LOG_FILE = os.path.join(DATA_PATH, "etl_log.txt")

def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{now}] {message}\n")
    print(f"[{now}] {message}")

def run_etl():
    log("Starting ETL process...")

    # Load datasets
    patients = pd.read_csv(f"{DATA_PATH}/patients.csv")
    doctors = pd.read_csv(f"{DATA_PATH}/doctors.csv")
    appointments = pd.read_csv(f"{DATA_PATH}/appointments.csv")
    wearables = pd.read_csv(f"{DATA_PATH}/wearables.csv")

    # Validate and clean
    patients.drop_duplicates(subset="patient_id", inplace=True)
    doctors.drop_duplicates(subset="doctor_id", inplace=True)
    appointments.dropna(subset=["patient_id", "doctor_id"], inplace=True)

    log(f"Loaded and cleaned datasets | Patients={len(patients)}, Doctors={len(doctors)}, Appts={len(appointments)}")

    # Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    patients.to_sql("patients", conn, if_exists="replace", index=False)
    doctors.to_sql("doctors", conn, if_exists="replace", index=False)
    appointments.to_sql("appointments", conn, if_exists="replace", index=False)
    wearables.to_sql("wearables", conn, if_exists="replace", index=False)
    conn.close()

    log("Data successfully updated in reminder_system.db")

    # Profile summary
    summary = {
        "patients": len(patients),
        "doctors": len(doctors),
        "appointments": len(appointments),
        "wearables": len(wearables),
        "last_run": datetime.now().isoformat()
    }
    json.dump(summary, open(f"{DATA_PATH}/etl_summary.json", "w"), indent=4)
    log("Summary saved to etl_summary.json")

    log("ETL pipeline completed.\n")

if __name__ == "__main__":
    run_etl()

from etl_logger import log_event

try:
    log_event("ETL", "Starting pipeline", "RUNNING")
    # existing ETL steps ...
    log_event("ETL", "Pipeline completed successfully", "SUCCESS")
except Exception as e:
    log_event("ETL", f"Pipeline failed: {e}", "FAILED")

