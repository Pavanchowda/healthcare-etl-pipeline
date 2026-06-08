import numpy as np


class PerformanceOptimizer:

    def optimize_memory(self, appointments_df, treatments_df):
        appointments_df = appointments_df.copy()
        treatments_df = treatments_df.copy()

        appointments_df["doctor_id"] = appointments_df["doctor_id"].astype("category")
        treatments_df["treatment_type"] = treatments_df["treatment_type"].astype("category")

        return appointments_df, treatments_df

    def vectorized_visit_duration(self, appointments_df):
        appointments_df = appointments_df.copy()

        start_times = appointments_df["start_time"].values
        end_times = appointments_df["end_time"].values

        duration_minutes = (
            end_times - start_times
        ) / np.timedelta64(1, "m")

        appointments_df["visit_duration_minutes"] = duration_minutes

        return appointments_df

    def vectorized_high_cost_outliers(self, treatments_df):
        treatments_df = treatments_df.copy()

        cost_values = treatments_df["cost"].to_numpy()

        threshold = np.percentile(cost_values, 99)

        treatments_df["is_high_cost_outlier"] = treatments_df["cost"] > threshold

        return treatments_df