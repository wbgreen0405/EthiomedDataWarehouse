-- models/transformed_contact_number.sql
{{ config(materialized='table') }}

WITH source_data AS (
    SELECT
        channel_id,
        contact_phone_numbers
    FROM {{ ref('transformed_medical_product') }} -- CHANGE THIS LINE
    WHERE contact_phone_numbers IS NOT NULL AND contact_phone_numbers != ''
)

SELECT DISTINCT ON (channel_id)
    channel_id,
    contact_phone_numbers
FROM source_data