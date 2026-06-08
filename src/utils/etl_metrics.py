class ETLMetrics:

    def __init__(self):
        self.metrics = {
            "patients_rows_extracted": 0,
            "appointments_rows_extracted": 0,
            "treatments_rows_extracted": 0,

            "patients_rows_transformed": 0,
            "appointments_rows_transformed": 0,
            "treatments_rows_transformed": 0,

            "patients_rows_loaded": 0,
            "appointments_rows_loaded": 0,
            "treatments_rows_loaded": 0,

            "invalid_patient_records": 0,
            "invalid_appointment_records": 0,
            "invalid_treatment_records": 0
        }

    def update_metric(self, metric_name, value):
        if metric_name in self.metrics:
            self.metrics[metric_name] = value
        else:
            raise KeyError(f"Metric '{metric_name}' does not exist")

    def get_metrics(self):
        return self.metrics

    def print_metrics(self):
        print("\n" + "=" * 50)
        print("ETL METRICS SUMMARY")
        print("=" * 50)

        for metric_name, value in self.metrics.items():
            print(f"{metric_name}: {value}")