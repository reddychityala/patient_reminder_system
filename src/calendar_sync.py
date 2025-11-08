import json
import random
from datetime import datetime, timedelta
import pandas as pd
import os

# ensure data folder exists
os.makedirs("data", exist_ok=True)


def generate_calendar(entity, n=10):
    """Generate mock free/busy slots for doctors or patients."""
    calendars = {}
    base_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    for i in range(1, n + 1):
        name = f"{entity}_{i}"
        slots = []
        for d in range(3):  # 3 days of availability
            day = base_date + timedelta(days=d)
            for slot in range(8):  # 8 working hours
                start = day + timedelta(hours=slot)
                end = start + timedelta(hours=1)
                status = random.choice(["free", "busy"])
                slots.append({
                    "date": day.strftime("%Y-%m-%d"),
                    "start": start.strftime("%H:%M"),
                    "end": end.strftime("%H:%M"),
                    "status": status
                })
        calendars[name] = slots
    return calendars

def find_common_free_slots(doctor_cal, patient_cal):
    """Find simple intersection of 'free' slots."""
    common = []
    for d_slots in doctor_cal.values():
        for p_slots in patient_cal.values():
            for d in d_slots:
                for p in p_slots:
                    if (d["date"] == p["date"] and
                        d["start"] == p["start"] and
                        d["status"] == "free" and
                        p["status"] == "free"):
                        common.append({
                            "date": d["date"],
                            "start": d["start"],
                            "end": d["end"]
                        })
    return pd.DataFrame(common)

if __name__ == "__main__":
    doctor_calendar = generate_calendar("doctor", n=10)
    patient_calendar = generate_calendar("patient", n=30)

    # save to JSON
    with open("/data/doctor_calendar.json", "w") as f:
        json.dump(doctor_calendar, f, indent=2)

    with open("/data/patient_calendar.json", "w") as f:
        json.dump(patient_calendar, f, indent=2)

    # find intersections for demo
    sample_common = find_common_free_slots(doctor_calendar, patient_calendar)
    print(f"Generated calendars. Found {len(sample_common)} common free slots.")
    print(sample_common.head())
