
  
    

  create  table "postgres"."public"."transformed_contact_number__dbt_tmp"
  
  
    as
  
  (
    -- models/transformed_contact_number.sql


WITH source_data AS (
    SELECT
        channel_id,
        contact_phone_numbers
    FROM "postgres"."public"."transformed_medical_product" -- CHANGE THIS LINE
    WHERE contact_phone_numbers IS NOT NULL AND contact_phone_numbers != ''
)

SELECT DISTINCT ON (channel_id)
    channel_id,
    contact_phone_numbers
FROM source_data
  );
  