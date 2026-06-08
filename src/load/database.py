import psycopg2


def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="healthcare_dw",
        user="postgres",
        password="Pavan@187"
    )

    return connection