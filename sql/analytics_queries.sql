-- 1. Most common treatments
SELECT
    treatment_type,
    COUNT(*) AS treatment_count
FROM fact_treatment
GROUP BY treatment_type
ORDER BY treatment_count DESC;


-- 2. Average visits per patient
SELECT
    AVG(visit_count) AS average_visits_per_patient
FROM (
    SELECT
        patient_id,
        COUNT(*) AS visit_count
    FROM dim_appointment
    GROUP BY patient_id
) AS patient_visits;


-- 3. Monthly appointment trends
SELECT
    DATE_TRUNC('month', start_time) AS appointment_month,
    COUNT(*) AS appointment_count
FROM dim_appointment
GROUP BY appointment_month
ORDER BY appointment_month;


-- 4. Total cost per patient
SELECT
    p.patient_id,
    p.patient_name,
    SUM(t.cost) AS total_cost
FROM dim_patient p
JOIN fact_treatment t
    ON p.patient_id = t.patient_id
GROUP BY p.patient_id, p.patient_name
ORDER BY total_cost DESC;


-- 5. Average treatment duration by type
SELECT
    treatment_type,
    AVG(duration_minutes) AS average_duration_minutes
FROM fact_treatment
GROUP BY treatment_type
ORDER BY average_duration_minutes DESC;


-- 6. Patients with overlapping appointments
SELECT
    patient_id,
    appointment_id,
    start_time,
    end_time,
    previous_end_time
FROM (
    SELECT
        patient_id,
        appointment_id,
        start_time,
        end_time,
        LAG(end_time) OVER (
            PARTITION BY patient_id
            ORDER BY start_time
        ) AS previous_end_time
    FROM dim_appointment
) AS overlap_check
WHERE start_time < previous_end_time;


-- 7. Patients with frequent visits (> 3 per month)
SELECT
    patient_id,
    DATE_TRUNC('month', start_time) AS appointment_month,
    COUNT(*) AS visit_count
FROM dim_appointment
GROUP BY patient_id, appointment_month
HAVING COUNT(*) > 3
ORDER BY visit_count DESC;


-- 8. Treatments per doctor
SELECT
    doctor_id,
    COUNT(*) AS treatment_count
FROM fact_treatment
GROUP BY doctor_id
ORDER BY treatment_count DESC;


-- 9. Treatment cost outliers - top 1%
SELECT
    *
FROM fact_treatment
WHERE cost >= (
    SELECT PERCENTILE_CONT(0.99)
    WITHIN GROUP (ORDER BY cost)
    FROM fact_treatment
)
ORDER BY cost DESC;


-- 10. Cohort analysis: patients by signup/month vs treatment frequency
SELECT
    DATE_TRUNC('month', p.dob) AS patient_birth_month,
    COUNT(t.treatment_id) AS treatment_frequency
FROM dim_patient p
LEFT JOIN fact_treatment t
    ON p.patient_id = t.patient_id
GROUP BY patient_birth_month
ORDER BY patient_birth_month;