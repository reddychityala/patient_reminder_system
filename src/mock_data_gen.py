import pandas as pd
from faker import Faker
import random, os, matplotlib.pyplot as plt

fake = Faker()

# --- FIXED PATH SETUP ---
# Get absolute path to the project root (one level above /src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)



def generate_patients(n=500):
    """Generate mock patient records"""
    genders = ['Male', 'Female', 'Other']
    marital_status = ['Single', 'Married', 'Divorced']
    channels = ['SMS', 'Email', 'Phone']

    patients = []
    for _ in range(n):
        patients.append({
            'patient_id': fake.uuid4(),
            'name': fake.name(),
            'age': random.randint(18, 90),
            'gender': random.choice(genders),
            'marital_status': random.choice(marital_status),
            'num_children': random.randint(0, 4),
            'preferred_channel': random.choice(channels),
            'city': fake.city(),
            'state': fake.state()
        })
    return pd.DataFrame(patients)


def generate_doctors(n=30):
    """Generate mock doctor records"""
    specialties = ['Cardiology', 'Dermatology', 'Pediatrics', 'Orthopedics', 'Neurology']
    doctors = []
    for _ in range(n):
        doctors.append({
            'doctor_id': fake.uuid4(),
            'name': fake.name(),
            'specialization': random.choice(specialties),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'availability': random.choice(['Mon-Fri', 'Mon-Sat'])
        })
    return pd.DataFrame(doctors)


if __name__ == "__main__":
    # create dataframes
    patients_df = generate_patients()
    doctors_df = generate_doctors()

    # save to csv
    patients_df.to_csv('../data/patients.csv', index=False)
    doctors_df.to_csv('../data/doctors.csv', index=False)

    # display summary
    print(f" Generated {len(patients_df)} patients and {len(doctors_df)} doctors.")
    print("Files saved in /data folder.")

    # quick visualization
    patients_df['age'].plot(kind='hist', bins=20, title='Age Distribution')
    plt.xlabel('Age')
    plt.show()

    patients_df['gender'].value_counts().plot(kind='bar', title='Gender Ratio')
    plt.show()
