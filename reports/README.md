# Healthcare ETL Pipeline

## Project Overview

This project implements a Healthcare ETL Pipeline using Medallion Architecture.

The objective is to clean, validate, transform, enrich, and load healthcare data into a dimensional model for analytics and reporting.

The project processes:

- Patients
- Appointments
- Treatments

and loads the data into:

- dim_patient
- dim_appointment
- dim_doctor
- fact_treatment

---

# Architecture

```text
Bronze Layer
    |
    v
Extract + Validation
    |
    v
Silver Layer
(Cleaned Data)
    |
    v
Transform + Enrichment
    |
    v
Gold Layer
(Dimensions + Facts)
    |
    v
PostgreSQL
    |
    v
Analytics Queries
```

---

# Medallion Architecture

## Bronze Layer

Raw source data.

Files:

- patients.csv
- appointments.csv
- treatments.csv

No modifications are performed.

---

## Silver Layer

Cleaned and validated datasets.

Tasks:

- Missing value handling
- Duplicate removal
- Invalid date correction
- Orphan record removal
- Data normalization

---

## Gold Layer

Analytics-ready dimension and fact tables.

Dimensions:

- dim_patient
- dim_appointment
- dim_doctor

Fact:

- fact_treatment

---

# Extract Phase

Validation checks:

- Missing columns
- Missing values
- Duplicate rows
- Duplicate IDs
- Null patient IDs
- Orphan appointments
- Orphan treatments
- Invalid dates
- Invalid timestamps

---

# Transform Phase

Transformations:

- Normalize patient names
- Standardize dates
- Standardize gender values
- Remove duplicates
- Remove invalid rows
- Calculate visit duration
- Calculate treatment cost metrics

Advanced transformations:

- Frequent visitor detection
- Overlapping appointments
- High-cost treatment outliers
- Monthly aggregations
- Dataset merging

---

# Load Phase

Database:

PostgreSQL

Tables:

- dim_patient
- dim_appointment
- dim_doctor
- fact_treatment
- etl_audit_log

Features:

- Primary keys
- Foreign keys
- Constraints
- Indexes
- Upsert logic

---

# Data Quality & Auditing

Metrics tracked:

- Rows extracted
- Rows transformed
- Rows loaded
- Missing records
- Invalid records
- Duplicate records

Audit results are stored in:

etl_audit_log

---

# Performance Optimizations

Python:

- NumPy vectorization
- Categorical data types

SQL:

- Indexed dimension keys
- Indexed fact keys
- Partitioning strategy for large fact tables

---

# Testing

Unit tests implemented:

- Visit duration computation
- Treatment cost aggregation
- Patient duplicate detection

---

# Technologies Used

Python

- Pandas
- NumPy
- Psycopg2
- Pytest

Database

- PostgreSQL

---

# Assumptions

- Patient IDs are unique after deduplication.
- Appointment IDs are unique after deduplication.
- Treatment IDs are unique after deduplication.
- Invalid dates are removed.
- Orphan records are removed during transformation.
- Missing treatment cost and duration values are replaced with default values.

---

# Author

Healthcare ETL Capstone Project