class MetricsCalculator:

    def calculate_visit_duration(self, appointments_df):
        appointments_df = appointments_df.copy()

        appointments_df["visit_duration_minutes"] = (
            appointments_df["end_time"] - appointments_df["start_time"]
        ).dt.total_seconds() / 60

        return appointments_df

    def treatment_cost_per_visit(self, treatments_df):
        return (
            treatments_df
            .groupby("appointment_id")["cost"]
            .sum()
            .reset_index()
            .rename(columns={"cost": "total_treatment_cost_per_visit"})
        )

    def treatment_cost_per_patient(self, treatments_df, appointments_df):
        treatment_appointments = treatments_df.merge(
            appointments_df[["appointment_id", "patient_id"]],
            on="appointment_id",
            how="inner"
        )

        return (
            treatment_appointments
            .groupby("patient_id")["cost"]
            .sum()
            .reset_index()
            .rename(columns={"cost": "total_treatment_cost_per_patient"})
        )