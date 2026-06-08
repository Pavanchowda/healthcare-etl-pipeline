import pandas as pd


class Transformer:

    def normalize_patients(self, patients_df):
        patients_df = patients_df.copy()

        patients_df["patient_name"] = (
            patients_df["patient_name"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

        patients_df["dob"] = pd.to_datetime(
            patients_df["dob"],
            errors="coerce"
        )

        patients_df["gender"] = (
            patients_df["gender"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.upper()
        )

        patients_df = patients_df.drop_duplicates(
            subset=["patient_id"],
            keep="first"
        )

        patients_df = patients_df.dropna(
            subset=["patient_id", "dob"]
        )

        return patients_df

    def clean_appointments(self, appointments_df, patients_df):
        appointments_df = appointments_df.copy()

        appointments_df["start_time"] = pd.to_datetime(
            appointments_df["start_time"],
            errors="coerce"
        )

        appointments_df["end_time"] = pd.to_datetime(
            appointments_df["end_time"],
            errors="coerce"
        )

        appointments_df = appointments_df.drop_duplicates(
            subset=["appointment_id"],
            keep="first"
        )

        appointments_df = appointments_df.dropna(
            subset=[
                "appointment_id",
                "patient_id",
                "doctor_id",
                "start_time",
                "end_time"
            ]
        )

        appointments_df = appointments_df[
            appointments_df["patient_id"].isin(patients_df["patient_id"])
        ]

        appointments_df = appointments_df[
            appointments_df["end_time"] > appointments_df["start_time"]
        ]

        return appointments_df

    def clean_treatments(self, treatments_df, appointments_df):
        treatments_df = treatments_df.copy()

        treatments_df["treatment_type"] = (
            treatments_df["treatment_type"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

        treatments_df["duration_minutes"] = pd.to_numeric(
            treatments_df["duration_minutes"],
            errors="coerce"
        )

        treatments_df["cost"] = pd.to_numeric(
            treatments_df["cost"],
            errors="coerce"
        )

        treatments_df["duration_minutes"] = treatments_df["duration_minutes"].fillna(0)
        treatments_df["cost"] = treatments_df["cost"].fillna(0)

        treatments_df = treatments_df.drop_duplicates(
            subset=["treatment_id"],
            keep="first"
        )

        treatments_df = treatments_df.dropna(
            subset=["treatment_id", "appointment_id"]
        )

        treatments_df = treatments_df[
            treatments_df["appointment_id"].isin(appointments_df["appointment_id"])
        ]

        return treatments_df