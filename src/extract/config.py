from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

BRONZE_PATH = BASE_DIR / "data" / "bronze"

PATIENTS_FILE = BRONZE_PATH / "patients.csv"
APPOINTMENTS_FILE = BRONZE_PATH / "appointments.csv"
TREATMENTS_FILE = BRONZE_PATH / "treatments.csv"