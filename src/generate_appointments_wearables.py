import pandas as pd
import numpy as np
import random, os
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# --- Project directories ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# --- Load existing patients & doctors ---
patients = pd.read_csv(os.path.join(DATA_DIR, "patients.csv"))
doctors = pd.read_csv(os.path.join(DATA_DIR, "doctors.csv"))

# --- Appointment generation ---
def generate_appointments(num_records=2000):
    appointments = []
    today = datetime.today()

    for _ in range(num_records):
        patient = patients.sample(1).iloc[0]
        doctor = doctors.sample(1).iloc[0]
        appt_date = today + timedelta(days=random.randint(1, 30))
        time_slot = random.choice(["09:00 AM", "10:30 AM", "12:00 PM", "02:00 PM", "04:00 PM"])
        status = random.choice(["Scheduled", "Completed", "Cancelled", "No Show"])

        appointments.append({
            "appointment_id": fake.uuid4(),
            "patient_id": patient["patient_id"],
            "doctor_id": doctor["doctor_id"],
            "appointment_date": appt_date.strftime("%Y-%m-%d"),
            "time_slot": time_slot,
            "status": status,
            "reason": random.choice(["Routine Checkup", "Follow-up", "Consultation", "Test Results"]),
            "created_at": today.strftime("%Y-%m-%d %H:%M:%S")
        })

    return pd.DataFrame(appointments)


# --- Wearable data generation ---
def generate_wearables():
    wearable_records = []
    for _, patient in patients.iterrows():
        start_date = datetime.today() - timedelta(days=7)
        for i in range(7):
            day = start_date + timedelta(days=i)
            wearable_records.append({
                "patient_id": patient["patient_id"],
                "date": day.strftime("%Y-%m-%d"),
                "steps": random.randint(3000, 15000),
                "heart_rate": random.randint(55, 120),
                "sleep_hours": round(random.uniform(4.5, 9.0), 1)
            })
    return pd.DataFrame(wearable_records)


if __name__ == "__main__":
    appts_df = generate_appointments()
    wearables_df = generate_wearables()

    appts_df.to_csv(os.path.join(DATA_DIR, "appointments.csv"), index=False)
    wearables_df.to_csv(os.path.join(DATA_DIR, "wearables.csv"), index=False)

    print(f"Generated {len(appts_df)} appointments and {len(wearables_df)} wearable records.")
    print("Files saved in /data folder.")
