class Aggregations:

    def frequent_visitors(self, appointments_df, visit_threshold=3):
        appointments_df = appointments_df.copy()

        appointments_df["appointment_month"] = (
            appointments_df["start_time"].dt.to_period("M").astype(str)
        )

        visit_counts = (
            appointments_df
            .groupby(["patient_id", "appointment_month"])
            .size()
            .reset_index(name="visit_count")
        )

        frequent_visitors = visit_counts[
            visit_counts["visit_count"] > visit_threshold
        ]

        return frequent_visitors

    def overlapping_appointments(self, appointments_df):
        appointments_df = appointments_df.copy()

        appointments_df = appointments_df.sort_values(
            by=["patient_id", "start_time"]
        )

        appointments_df["previous_end_time"] = (
            appointments_df
            .groupby("patient_id")["end_time"]
            .shift(1)
        )

        overlapping = appointments_df[
            appointments_df["start_time"] < appointments_df["previous_end_time"]
        ]

        return overlapping

    def monthly_appointment_counts(self, appointments_df):
        appointments_df = appointments_df.copy()

        appointments_df["appointment_month"] = (
            appointments_df["start_time"].dt.to_period("M").astype(str)
        )

        return (
            appointments_df
            .groupby("appointment_month")
            .size()
            .reset_index(name="appointment_count")
        )

    def monthly_treatment_counts(self, treatments_df, appointments_df):
        treatment_appointments = treatments_df.merge(
            appointments_df[["appointment_id", "start_time"]],
            on="appointment_id",
            how="inner"
        )

        treatment_appointments["treatment_month"] = (
            treatment_appointments["start_time"].dt.to_period("M").astype(str)
        )

        return (
            treatment_appointments
            .groupby("treatment_month")
            .size()
            .reset_index(name="treatment_count")
        )