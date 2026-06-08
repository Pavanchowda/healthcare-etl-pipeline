from extract.config import (
    PATIENTS_FILE,
    APPOINTMENTS_FILE,
    TREATMENTS_FILE
)

from healthcare_etl import HealthcareETL
from load.database import get_connection


connection = get_connection()

etl = HealthcareETL(
    PATIENTS_FILE,
    APPOINTMENTS_FILE,
    TREATMENTS_FILE
)

etl.run(connection)

connection.close()