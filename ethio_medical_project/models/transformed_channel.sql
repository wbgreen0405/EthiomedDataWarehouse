-- models/transformed_channel.sql
{{ config(materialized='table') }}

WITH source_data AS (
    SELECT
        channel_id,
        channel_username,
        channel_title
    FROM {{ ref('transformed_medical_product') }} -- CHANGE THIS LINE
    WHERE contact_phone_numbers IS NOT NULL AND contact_phone_numbers != ''
)

SELECT DISTINCT ON (channel_id)
    channel_id,
    channel_username,
    channel_title
FROM source_data