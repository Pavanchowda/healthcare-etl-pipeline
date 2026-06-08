import numpy as np


class StatisticsSummary:

    def average_treatment_cost(self, treatments_df):
        return np.mean(treatments_df["cost"])

    def median_visit_duration(self, appointments_df):
        return np.median(appointments_df["visit_duration_minutes"])

    def standard_deviation_treatment_duration(self, treatments_df):
        return np.std(treatments_df["duration_minutes"])

    def high_cost_treatment_outliers(self, treatments_df):
        cost_threshold = np.percentile(treatments_df["cost"], 99)

        outliers = treatments_df[
            treatments_df["cost"] > cost_threshold
        ]

        return outliers