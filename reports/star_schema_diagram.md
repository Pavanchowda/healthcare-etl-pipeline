# Healthcare Star Schema

```text
                    +------------------+
                    |   dim_patient    |
                    +------------------+
                    | patient_id (PK)  |
                    | patient_name     |
                    | dob              |
                    | gender           |
                    +------------------+
                             |
                             |
                             |
                             v

                    +------------------+
                    | dim_appointment  |
                    +------------------+
                    | appointment_id   |
                    | patient_id (FK)  |
                    | doctor_id (FK)   |
                    | start_time       |
                    | end_time         |
                    | visit_duration   |
                    +------------------+
                             |
                             |
                             |
                             v

                    +------------------+
                    | fact_treatment   |
                    +------------------+
                    | treatment_id     |
                    | appointment_id   |
                    | patient_id       |
                    | doctor_id        |
                    | treatment_type   |
                    | duration_minutes |
                    | cost             |
                    +------------------+
                             ^
                             |
                             |
                    +------------------+
                    |   dim_doctor     |
                    +------------------+
                    | doctor_id (PK)   |
                    +------------------+
```

## Fact Table

### fact_treatment

Measures:
- cost
- duration_minutes

Keys:
- treatment_id
- appointment_id
- patient_id
- doctor_id

## Dimension Tables

### dim_patient
- patient_id
- patient_name
- dob
- gender

### dim_appointment
- appointment_id
- patient_id
- doctor_id
- start_time
- end_time
- visit_duration_minutes

### dim_doctor
- doctor_id

## Relationships

1. dim_patient → dim_appointment
2. dim_doctor → dim_appointment
3. dim_appointment → fact_treatment
4. dim_patient → fact_treatment
5. dim_doctor → fact_treatment
```