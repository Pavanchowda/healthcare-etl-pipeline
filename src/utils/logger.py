import logging
import os


class ETLLogger:

    def __init__(self, log_file="logs/healthcare_etl.log"):

        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger("HealthcareETL")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)