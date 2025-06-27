-- models/ethio_medical.sql
{{ config(materialized='table') }}

WITH source_data AS (
    SELECT *
    FROM {{ source('medical_data', 'ethio_medical') }}  -- Use DBT's source function
)

SELECT
    channel_id,
    channel_title,
    lower(channel_username) AS channel_username,
    message_id,
    "message", -- Assuming you've already changed this to lowercase 'message'
    date,
    media_path
FROM source_data
WHERE "message" IS NOT NULL
-- Remove the semicolon from the line below:
AND media_path IS NOT NULL
