import pandas as pd

from src.extract.validators import DataValidator


def test_duplicate_patient_detection():
    validator = DataValidator()

    patients_df = pd.DataFrame({
        "patient_id": [1, 1, 2, 3]
    })

    duplicates = validator.find_duplicate_ids(
        patients_df,
        "patient_id"
    )

    assert len(duplicates) == 2