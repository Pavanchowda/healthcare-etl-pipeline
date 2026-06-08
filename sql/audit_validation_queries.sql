-- 1. Validate no orphan treatments
SELECT
    t.treatment_id,
    t.appointment_id
FROM fact_treatment t
LEFT JOIN dim_appointment a
    ON t.appointment_id = a.appointment_id
WHERE a.appointment_id IS NULL;


-- 2. Validate no duplicate appointment IDs
SELECT
    appointment_id,
    COUNT(*) AS duplicate_count
FROM dim_appointment
GROUP BY appointment_id
HAVING COUNT(*) > 1;


-- 3. Validate appointment durations
SELECT
    appointment_id,
    start_time,
    end_time,
    visit_duration_minutes
FROM dim_appointment
WHERE visit_duration_minutes <= 0
   OR end_time <= start_time;