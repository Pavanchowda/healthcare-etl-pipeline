import pandas as pd


class DataMerger:

    def merge_patients_appointments(
            self,
            patients_df,
            appointments_df
    ):
        merged_df = pd.merge(
            appointments_df,
            patients_df,
            on="patient_id",
            how="inner"
        )

        return merged_df

    def merge_treatments_appointments(
            self,
            treatments_df,
            appointments_df
    ):
        merged_df = pd.merge(
            treatments_df,
            appointments_df,
            on="appointment_id",
            how="inner"
        )

        return merged_df

    def create_complete_healthcare_dataset(
            self,
            patients_df,
            appointments_df,
            treatments_df
    ):
        patient_appointments = pd.merge(
            appointments_df,
            patients_df,
            on="patient_id",
            how="inner"
        )

        complete_dataset = pd.merge(
            treatments_df,
            patient_appointments,
            on="appointment_id",
            how="inner"
        )

        return complete_dataset