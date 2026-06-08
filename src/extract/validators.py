class DataValidator:

    def validate_columns(self, dataframe, required_columns):
        missing_columns = []

        for column in required_columns:
            if column not in dataframe.columns:
                missing_columns.append(column)

        return missing_columns

    def find_missing_values(self, dataframe):
        return dataframe.isnull().sum()

    def find_duplicates(self, dataframe):
        return dataframe.duplicated().sum()

    def find_duplicate_ids(self, dataframe, id_column):
        return dataframe[dataframe.duplicated(subset=[id_column], keep=False)]

    def find_null_patient_ids(self, appointments_df):
        return appointments_df[appointments_df["patient_id"].isnull()]

    def find_orphan_appointments(self, appointments_df, patients_df):
        valid_patient_ids = set(patients_df["patient_id"])

        orphan_appointments = appointments_df[
            ~appointments_df["patient_id"].isin(valid_patient_ids)
        ]

        return orphan_appointments

    def find_orphan_treatments(self, treatments_df, appointments_df):
        valid_appointment_ids = set(appointments_df["appointment_id"])

        orphan_treatments = treatments_df[
            ~treatments_df["appointment_id"].isin(valid_appointment_ids)
        ]

        return orphan_treatments

    def find_invalid_dates(self, dataframe, date_column):
        converted_dates = dataframe[date_column].apply(
            lambda value: value if str(value) != "nan" else None
        )

        invalid_dates = []

        for index, value in converted_dates.items():
            try:
                if value is not None:
                    import pandas as pd
                    pd.to_datetime(value)
            except Exception:
                invalid_dates.append(index)

        return dataframe.loc[invalid_dates]

    def find_invalid_timestamps(self, dataframe, timestamp_column):
        invalid_rows = []

        for index, value in dataframe[timestamp_column].items():
            try:
                import pandas as pd
                pd.to_datetime(value)
            except Exception:
                invalid_rows.append(index)

        return dataframe.loc[invalid_rows]