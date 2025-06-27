-- models/transformed_product_images.sql


WITH source_data AS (
    SELECT
        product_id, -- CHANGED FROM message_id TO product_id
        media_path
    FROM "postgres"."public"."transformed_medical_product"
    WHERE media_path IS NOT NULL AND media_path != ''
)

SELECT
    product_id, -- CHANGED FROM message_id TO product_id
    media_path AS image_path
FROM source_data