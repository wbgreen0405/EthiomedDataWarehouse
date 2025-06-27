
  
    

  create  table "postgres"."public"."ethio_medical__dbt_tmp"
  
  
    as
  
  (
    -- models/ethio_medical.sql


WITH source_data AS (
    SELECT *
    FROM "postgres"."public"."ethio_medical"  -- Use DBT's source function
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
  );
  