from pathlib import Path

from extract.extract import Extractor
from extract.validators import DataValidator

from transform.transform import Transformer
from transform.metrics import MetricsCalculator
from transform.statistics_summary import StatisticsSummary
from transform.aggregations import Aggregations
from transform.mergers import DataMerger
from transform.optimization import PerformanceOptimizer

from utils.logger import ETLLogger
from utils.etl_metrics import ETLMetrics

from load.loader import DataLoader


class Patient:
    def __init__(self, patient_id, name, dob, gender):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.gender = gender


class Appointment:
    def __init__(self, appointment_id, patient_id, start_time, end_time, doctor_id):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.start_time = start_time
        self.end_time = end_time
        self.doctor_id = doctor_id


class HealthcareETL:

    def __init__(self, patients_file, appointments_file, treatments_file):
        self.patients_file = patients_file
        self.appointments_file = appointments_file
        self.treatments_file = treatments_file

        self.extractor = Extractor()
        self.validator = DataValidator()
        self.transformer = Transformer()
        self.metrics_calculator = MetricsCalculator()
        self.statistics = StatisticsSummary()
        self.aggregations = Aggregations()
        self.merger = DataMerger()
        self.optimizer = PerformanceOptimizer()
        self.loader = DataLoader()

        self.logger = ETLLogger()
        self.etl_metrics = ETLMetrics()

        self.patients_df = None
        self.appointments_df = None
        self.treatments_df = None

        self.cleaned_patients_df = None
        self.cleaned_appointments_df = None
        self.cleaned_treatments_df = None

        self.silver_dir = Path("data/silver")
        self.gold_dir = Path("data/gold")

        self.silver_dir.mkdir(parents=True, exist_ok=True)
        self.gold_dir.mkdir(parents=True, exist_ok=True)

    def extract(self):
        self.logger.info("Starting Extract phase")

        self.patients_df = self.extractor.load_patients(self.patients_file)
        self.appointments_df = self.extractor.load_appointments(self.appointments_file)
        self.treatments_df = self.extractor.load_treatments(self.treatments_file)

        self.etl_metrics.update_metric(
            "patients_rows_extracted",
            len(self.patients_df)
        )

        self.etl_metrics.update_metric(
            "appointments_rows_extracted",
            len(self.appointments_df)
        )

        self.etl_metrics.update_metric(
            "treatments_rows_extracted",
            len(self.treatments_df)
        )

        self.logger.info("Extract phase completed")

    def validate(self):
        self.logger.info("Starting Validation phase")

        duplicate_patient_ids = self.validator.find_duplicate_ids(
            self.patients_df,
            "patient_id"
        )

        duplicate_appointment_ids = self.validator.find_duplicate_ids(
            self.appointments_df,
            "appointment_id"
        )

        duplicate_treatment_ids = self.validator.find_duplicate_ids(
            self.treatments_df,
            "treatment_id"
        )

        null_patient_ids = self.validator.find_null_patient_ids(
            self.appointments_df
        )

        orphan_appointments = self.validator.find_orphan_appointments(
            self.appointments_df,
            self.patients_df
        )

        orphan_treatments = self.validator.find_orphan_treatments(
            self.treatments_df,
            self.appointments_df
        )

        invalid_dob_dates = self.validator.find_invalid_dates(
            self.patients_df,
            "dob"
        )

        invalid_end_times = self.validator.find_invalid_timestamps(
            self.appointments_df,
            "end_time"
        )

        self.etl_metrics.update_metric(
            "invalid_patient_records",
            len(duplicate_patient_ids) + len(invalid_dob_dates)
        )

        self.etl_metrics.update_metric(
            "invalid_appointment_records",
            len(duplicate_appointment_ids)
            + len(null_patient_ids)
            + len(orphan_appointments)
            + len(invalid_end_times)
        )

        self.etl_metrics.update_metric(
            "invalid_treatment_records",
            len(duplicate_treatment_ids) + len(orphan_treatments)
        )

        self.logger.info("Validation phase completed")

    def transform(self):
        self.logger.info("Starting Transform phase")

        self.cleaned_patients_df = self.transformer.normalize_patients(
            self.patients_df
        )

        self.cleaned_appointments_df = self.transformer.clean_appointments(
            self.appointments_df,
            self.cleaned_patients_df
        )

        self.cleaned_appointments_df = self.metrics_calculator.calculate_visit_duration(
            self.cleaned_appointments_df
        )

        self.cleaned_treatments_df = self.transformer.clean_treatments(
            self.treatments_df,
            self.cleaned_appointments_df
        )

        self.cleaned_appointments_df, self.cleaned_treatments_df = self.optimizer.optimize_memory(
            self.cleaned_appointments_df,
            self.cleaned_treatments_df
        )

        self.cleaned_patients_df.to_csv(
            self.silver_dir / "cleaned_patients.csv",
            index=False
        )

        self.cleaned_appointments_df.to_csv(
            self.silver_dir / "cleaned_appointments.csv",
            index=False
        )

        self.cleaned_treatments_df.to_csv(
            self.silver_dir / "cleaned_treatments.csv",
            index=False
        )

        self.etl_metrics.update_metric(
            "patients_rows_transformed",
            len(self.cleaned_patients_df)
        )

        self.etl_metrics.update_metric(
            "appointments_rows_transformed",
            len(self.cleaned_appointments_df)
        )

        self.etl_metrics.update_metric(
            "treatments_rows_transformed",
            len(self.cleaned_treatments_df)
        )

        self.logger.info("Transform phase completed")

    def enrich(self):
        self.logger.info("Starting Enrich phase")

        treatment_cost_per_visit = self.metrics_calculator.treatment_cost_per_visit(
            self.cleaned_treatments_df
        )

        treatment_cost_per_patient = self.metrics_calculator.treatment_cost_per_patient(
            self.cleaned_treatments_df,
            self.cleaned_appointments_df
        )

        frequent_visitors = self.aggregations.frequent_visitors(
            self.cleaned_appointments_df
        )

        overlapping_appointments = self.aggregations.overlapping_appointments(
            self.cleaned_appointments_df
        )

        monthly_appointments = self.aggregations.monthly_appointment_counts(
            self.cleaned_appointments_df
        )

        monthly_treatments = self.aggregations.monthly_treatment_counts(
            self.cleaned_treatments_df,
            self.cleaned_appointments_df
        )

        high_cost_outliers = self.statistics.high_cost_treatment_outliers(
            self.cleaned_treatments_df
        )

        complete_healthcare_dataset = self.merger.create_complete_healthcare_dataset(
            self.cleaned_patients_df,
            self.cleaned_appointments_df,
            self.cleaned_treatments_df
        )

        treatment_cost_per_visit.to_csv(
            self.gold_dir / "treatment_cost_per_visit.csv",
            index=False
        )

        treatment_cost_per_patient.to_csv(
            self.gold_dir / "treatment_cost_per_patient.csv",
            index=False
        )

        frequent_visitors.to_csv(
            self.gold_dir / "frequent_visitors.csv",
            index=False
        )

        overlapping_appointments.to_csv(
            self.gold_dir / "overlapping_appointments.csv",
            index=False
        )

        monthly_appointments.to_csv(
            self.gold_dir / "monthly_appointments.csv",
            index=False
        )

        monthly_treatments.to_csv(
            self.gold_dir / "monthly_treatments.csv",
            index=False
        )

        high_cost_outliers.to_csv(
            self.gold_dir / "high_cost_outliers.csv",
            index=False
        )

        complete_healthcare_dataset.to_csv(
            self.gold_dir / "complete_healthcare_dataset.csv",
            index=False
        )

        self.logger.info("Enrich phase completed")

    def load(self, db_connection=None):
        self.logger.info("Starting Load phase")

        if db_connection is None:
            self.logger.warning(
                "No database connection provided. Skipping PostgreSQL load."
            )
            return

        self.loader.create_tables(db_connection)

        self.loader.upsert_dim_patient(
            db_connection,
            self.cleaned_patients_df
        )

        self.loader.upsert_dim_doctor(
            db_connection,
            self.cleaned_appointments_df
        )

        self.loader.upsert_dim_appointment(
            db_connection,
            self.cleaned_appointments_df
        )

        self.loader.insert_fact_treatment(
            db_connection,
            self.cleaned_treatments_df,
            self.cleaned_appointments_df
        )

        self.etl_metrics.update_metric(
            "patients_rows_loaded",
            len(self.cleaned_patients_df)
        )

        self.etl_metrics.update_metric(
            "appointments_rows_loaded",
            len(self.cleaned_appointments_df)
        )

        self.etl_metrics.update_metric(
            "treatments_rows_loaded",
            len(self.cleaned_treatments_df)
        )

        self.logger.info("Load phase completed")

    def run(self, db_connection=None):
        self.logger.info("Healthcare ETL Pipeline started")

        self.extract()
        self.validate()
        self.transform()
        self.enrich()
        self.load(db_connection)

        self.etl_metrics.print_metrics()

        self.logger.info("Healthcare ETL Pipeline completed")