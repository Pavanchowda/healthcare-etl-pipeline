from extract.config import (
    PATIENTS_FILE,
    APPOINTMENTS_FILE,
    TREATMENTS_FILE
)

from extract.extract import Extractor

from extract.schema import (
    PATIENT_COLUMNS,
    APPOINTMENT_COLUMNS,
    TREATMENT_COLUMNS
)

from extract.validators import DataValidator
from extract.quality_report import QualityReport


extractor = Extractor()
validator = DataValidator()
report = QualityReport()


# =========================
# 1. EXTRACT CSV FILES
# =========================

patients_df = extractor.load_patients(PATIENTS_FILE)
appointments_df = extractor.load_appointments(APPOINTMENTS_FILE)
treatments_df = extractor.load_treatments(TREATMENTS_FILE)


# =========================
# 2. VALIDATE MISSING COLUMNS
# =========================

patient_missing_columns = validator.validate_columns(
    patients_df,
    PATIENT_COLUMNS
)

appointment_missing_columns = validator.validate_columns(
    appointments_df,
    APPOINTMENT_COLUMNS
)

treatment_missing_columns = validator.validate_columns(
    treatments_df,
    TREATMENT_COLUMNS
)


report.show_missing_columns(
    "Patients",
    patient_missing_columns
)

report.show_missing_columns(
    "Appointments",
    appointment_missing_columns
)

report.show_missing_columns(
    "Treatments",
    treatment_missing_columns
)


# =========================
# 3. CHECK MISSING VALUES
# =========================

patient_missing_values = validator.find_missing_values(patients_df)
appointment_missing_values = validator.find_missing_values(appointments_df)
treatment_missing_values = validator.find_missing_values(treatments_df)


report.show_missing_values(
    "Patients",
    patient_missing_values
)

report.show_missing_values(
    "Appointments",
    appointment_missing_values
)

report.show_missing_values(
    "Treatments",
    treatment_missing_values
)


# =========================
# 4. CHECK DUPLICATES
# =========================

patient_duplicates = validator.find_duplicates(patients_df)
appointment_duplicates = validator.find_duplicates(appointments_df)
treatment_duplicates = validator.find_duplicates(treatments_df)


report.show_duplicate_count(
    "Patients",
    patient_duplicates
)

report.show_duplicate_count(
    "Appointments",
    appointment_duplicates
)

report.show_duplicate_count(
    "Treatments",
    treatment_duplicates
)

# =========================
# 5. CHECK DUPLICATE IDS
# =========================

duplicate_patient_ids = validator.find_duplicate_ids(
    patients_df,
    "patient_id"
)

duplicate_appointment_ids = validator.find_duplicate_ids(
    appointments_df,
    "appointment_id"
)

duplicate_treatment_ids = validator.find_duplicate_ids(
    treatments_df,
    "treatment_id"
)


report.show_invalid_records(
    "Duplicate Patient IDs",
    duplicate_patient_ids
)

report.show_invalid_records(
    "Duplicate Appointment IDs",
    duplicate_appointment_ids
)

report.show_invalid_records(
    "Duplicate Treatment IDs",
    duplicate_treatment_ids
)


# =========================
# 6. NULL PATIENT IDS
# =========================

null_patient_ids = validator.find_null_patient_ids(
    appointments_df
)

report.show_invalid_records(
    "Null Patient IDs",
    null_patient_ids
)

# =========================
# 7. ORPHAN APPOINTMENTS
# =========================

orphan_appointments = validator.find_orphan_appointments(
    appointments_df,
    patients_df
)

report.show_invalid_records(
    "Orphan Appointments",
    orphan_appointments
)

# =========================
# 8. ORPHAN TREATMENTS
# =========================

orphan_treatments = validator.find_orphan_treatments(
    treatments_df,
    appointments_df
)

report.show_invalid_records(
    "Orphan Treatments",
    orphan_treatments
)

# =========================
# 9. INVALID DOB DATES
# =========================

invalid_dob_dates = validator.find_invalid_dates(
    patients_df,
    "dob"
)

report.show_invalid_records(
    "Invalid DOB Dates",
    invalid_dob_dates
)

# =========================
# 10. INVALID TIMESTAMPS
# =========================

invalid_end_times = validator.find_invalid_timestamps(
    appointments_df,
    "end_time"
)

report.show_invalid_records(
    "Invalid Appointment End Times",
    invalid_end_times
)