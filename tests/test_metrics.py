import pandas as pd

from src.transform.metrics import MetricsCalculator


def test_visit_duration_computation():
    metrics = MetricsCalculator()

    appointments_df = pd.DataFrame({
        "appointment_id": [1],
        "start_time": ["2025-01-01 10:00:00"],
        "end_time": ["2025-01-01 11:00:00"]
    })

    appointments_df["start_time"] = pd.to_datetime(appointments_df["start_time"])
    appointments_df["end_time"] = pd.to_datetime(appointments_df["end_time"])

    result = metrics.calculate_visit_duration(appointments_df)

    assert result["visit_duration_minutes"].iloc[0] == 60


def test_treatment_cost_aggregation():
    metrics = MetricsCalculator()

    treatments_df = pd.DataFrame({
        "appointment_id": [1, 1, 1],
        "cost": [100, 200, 300]
    })

    result = metrics.treatment_cost_per_visit(treatments_df)

    assert result["total_treatment_cost_per_visit"].iloc[0] == 600