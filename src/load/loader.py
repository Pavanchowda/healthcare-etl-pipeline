from load.ddl import CREATE_TABLES_SQL


class DataLoader:

    def create_tables(self, connection):
        cursor = connection.cursor()

        cursor.execute(CREATE_TABLES_SQL)

        connection.commit()
        cursor.close()

        print("Database tables created successfully")

    def upsert_dim_patient(self, connection, patients_df):
        cursor = connection.cursor()

        for _, row in patients_df.iterrows():
            cursor.execute(
                """
                INSERT INTO dim_patient (
                    patient_id,
                    patient_name,
                    dob,
                    gender
                )
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (patient_id)
                DO UPDATE SET
                    patient_name = EXCLUDED.patient_name,
                    dob = EXCLUDED.dob,
                    gender = EXCLUDED.gender;
                """,
                (
                    int(row["patient_id"]),
                    row["patient_name"],
                    row["dob"],
                    row["gender"]
                )
            )

        connection.commit()
        cursor.close()

    def upsert_dim_doctor(self, connection, appointments_df):
        cursor = connection.cursor()

        doctor_ids = appointments_df["doctor_id"].drop_duplicates()

        for doctor_id in doctor_ids:
            cursor.execute(
                """
                INSERT INTO dim_doctor (doctor_id)
                VALUES (%s)
                ON CONFLICT (doctor_id)
                DO NOTHING;
                """,
                (int(doctor_id),)
            )

        connection.commit()
        cursor.close()

    def upsert_dim_appointment(self, connection, appointments_df):
        cursor = connection.cursor()

        for _, row in appointments_df.iterrows():
            cursor.execute(
                """
                INSERT INTO dim_appointment (
                    appointment_id,
                    patient_id,
                    doctor_id,
                    start_time,
                    end_time,
                    visit_duration_minutes
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (appointment_id)
                DO UPDATE SET
                    patient_id = EXCLUDED.patient_id,
                    doctor_id = EXCLUDED.doctor_id,
                    start_time = EXCLUDED.start_time,
                    end_time = EXCLUDED.end_time,
                    visit_duration_minutes = EXCLUDED.visit_duration_minutes;
                """,
                (
                    int(row["appointment_id"]),
                    int(row["patient_id"]),
                    int(row["doctor_id"]),
                    row["start_time"],
                    row["end_time"],
                    float(row["visit_duration_minutes"])
                )
            )

        connection.commit()
        cursor.close()

    def insert_audit_log(self, connection, metrics):
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO etl_audit_log (
                pipeline_name,
                rows_extracted,
                rows_transformed,
                rows_loaded,
                missing_records,
                invalid_records,
                duplicate_records,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                "Healthcare ETL Pipeline",
                metrics.get("rows_extracted", 0),
                metrics.get("rows_transformed", 0),
                metrics.get("rows_loaded", 0),
                metrics.get("missing_records", 0),
                metrics.get("invalid_records", 0),
                metrics.get("duplicate_records", 0),
                metrics.get("status", "SUCCESS")
            )
        )

        connection.commit()
        cursor.close()

    def insert_fact_treatment(self, connection, treatments_df, appointments_df):
        cursor = connection.cursor()

        fact_df = treatments_df.merge(
            appointments_df[
                [
                    "appointment_id",
                    "patient_id",
                    "doctor_id"
                ]
            ],
            on="appointment_id",
            how="inner"
        )

        for _, row in fact_df.iterrows():
            cursor.execute(
                """
                INSERT INTO fact_treatment (
                    treatment_id,
                    appointment_id,
                    patient_id,
                    doctor_id,
                    treatment_type,
                    duration_minutes,
                    cost
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (treatment_id)
                DO UPDATE SET
                    appointment_id = EXCLUDED.appointment_id,
                    patient_id = EXCLUDED.patient_id,
                    doctor_id = EXCLUDED.doctor_id,
                    treatment_type = EXCLUDED.treatment_type,
                    duration_minutes = EXCLUDED.duration_minutes,
                    cost = EXCLUDED.cost;
                """,
                (
                    int(row["treatment_id"]),
                    int(row["appointment_id"]),
                    int(row["patient_id"]),
                    int(row["doctor_id"]),
                    row["treatment_type"],
                    float(row["duration_minutes"]),
                    float(row["cost"])
                )
            )

        connection.commit()
        cursor.close()