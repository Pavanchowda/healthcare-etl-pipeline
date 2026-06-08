CREATE_TABLES_SQL = """

CREATE TABLE IF NOT EXISTS dim_patient (
    patient_id INTEGER PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_doctor (
    doctor_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS dim_appointment (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    visit_duration_minutes NUMERIC NOT NULL,

    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (patient_id)
        REFERENCES dim_patient(patient_id),

    CONSTRAINT fk_appointment_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES dim_doctor(doctor_id)
);

CREATE TABLE IF NOT EXISTS fact_treatment (
    treatment_id INTEGER PRIMARY KEY,
    appointment_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    treatment_type VARCHAR(100) NOT NULL,
    duration_minutes NUMERIC NOT NULL,
    cost NUMERIC(10, 2) NOT NULL,

    CONSTRAINT fk_treatment_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES dim_appointment(appointment_id),

    CONSTRAINT fk_treatment_patient
        FOREIGN KEY (patient_id)
        REFERENCES dim_patient(patient_id),

    CONSTRAINT fk_treatment_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES dim_doctor(doctor_id)
);

CREATE TABLE IF NOT EXISTS etl_audit_log (
    audit_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    rows_extracted INTEGER,
    rows_transformed INTEGER,
    rows_loaded INTEGER,

    missing_records INTEGER,
    invalid_records INTEGER,
    duplicate_records INTEGER,

    status VARCHAR(50) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dim_appointment_patient_id
ON dim_appointment(patient_id);

CREATE INDEX IF NOT EXISTS idx_fact_treatment_appointment_id
ON fact_treatment(appointment_id);

CREATE INDEX IF NOT EXISTS idx_fact_treatment_patient_id
ON fact_treatment(patient_id);

CREATE INDEX IF NOT EXISTS idx_fact_treatment_treatment_id
ON fact_treatment(treatment_id);

"""