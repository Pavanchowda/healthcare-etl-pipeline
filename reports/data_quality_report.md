# Data Quality Report

## Project
Healthcare ETL Pipeline using Medallion Architecture.

## Source Files
- patients.csv
- appointments.csv
- treatments.csv

## Data Quality Checks Performed

### 1. Missing Columns
All required columns were validated for:
- Patients
- Appointments
- Treatments

Result:
- No missing columns found.

### 2. Missing Values

Patients:
- patient_name: 62 missing
- gender: 373 missing

Appointments:
- patient_id: 277 missing

Treatments:
- duration_minutes: 350 missing
- cost: 366 missing

### 3. Duplicate Records

Full duplicate rows:
- Patients: 0
- Appointments: 0
- Treatments: 0

Duplicate IDs:
- Duplicate Patient IDs: 48
- Duplicate Appointment IDs: 276
- Duplicate Treatment IDs: 360

### 4. Null Patient IDs

Appointments with null patient_id:
- 277 records

### 5. Orphan Records

Orphan appointments:
- 820 records

Orphan treatments:
- 353 records

### 6. Invalid Dates

Invalid patient DOB values:
- 62 records

Invalid appointment timestamps:
- Detected using timestamp validation logic.

## Cleaning Actions

The Silver layer removes or fixes:
- Duplicate IDs
- Invalid DOB values
- Invalid appointment timestamps
- Orphan appointments
- Orphan treatments
- Missing treatment cost
- Missing treatment duration

## Output Layers

Bronze:
- Raw CSV files

Silver:
- Cleaned patient, appointment, and treatment data

Gold:
- Dimension and fact tables for analytics