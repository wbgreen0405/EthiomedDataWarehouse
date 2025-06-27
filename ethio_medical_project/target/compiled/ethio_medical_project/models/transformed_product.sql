-- models/transformed_product.sql


WITH source_data AS (
    SELECT
        product_id,
        product_name, -- ADDED: Ensure this is selected from transformed_medical_product
        price_in_birr,
        channel_id,
        -- Assuming 'date' is also available in transformed_medical_product
        date -- Ensure this column exists in transformed_medical_product
    FROM "postgres"."public"."transformed_medical_product" -- CRITICAL CHANGE: Use ref() not source()
)

SELECT
    product_id,
    product_name, -- ADDED: Ensure this is here
    price_in_birr,
    channel_id,
    date
FROM source_data
-- Add any specific transformations or filters for transformed_product here