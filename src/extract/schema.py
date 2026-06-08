PATIENT_COLUMNS = [
    "patient_id",
    "patient_name",
    "dob",
    "gender"
]

APPOINTMENT_COLUMNS = [
    "appointment_id",
    "patient_id",
    "doctor_id",
    "start_time",
    "end_time"
]

TREATMENT_COLUMNS = [
    "treatment_id",
    "appointment_id",
    "treatment_type",
    "duration_minutes",
    "cost"
]