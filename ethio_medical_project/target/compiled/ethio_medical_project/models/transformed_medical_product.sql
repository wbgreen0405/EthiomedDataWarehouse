

WITH source_data AS (
    SELECT *
    FROM "postgres"."public"."ethio_medical"
),
phone_extracted AS (
    SELECT
        channel_id,
        message_id,
        channel_title,
        lower(channel_username) AS channel_username,
        "message", -- Ensure this is lowercase
        date,
        media_path,
        array_to_string(ARRAY(
            SELECT regexp_replace(unnest(regexp_matches("message", '09\s*[0-9]{8}', 'g')), '\s+', '', 'g')
        ), ', ') AS phone_numbers,
        regexp_replace(
            "message",
            '09\s*[0-9]{8}',
            '',
            'g'
        ) AS cleaned_message
    FROM source_data
),
product_price_extracted AS (
    SELECT
        channel_id,
        message_id,
        channel_title,
        channel_username,
        date,
        TRIM(cleaned_message) AS cleaned_message,
        phone_numbers,
        regexp_matches(cleaned_message, '^(.*?)\s*(?:price|Price|PRICE)\s*(\d+)\s*(birr|ETB)', 'g') AS matches,
        media_path,
        ROW_NUMBER() OVER (PARTITION BY message_id ORDER BY date DESC) AS rn
    FROM phone_extracted
)

SELECT
    channel_id,
    message_id AS product_id,
    channel_title,
    channel_username,
    date,
    TRIM(matches[1]) AS product_name,
    CAST(TRIM(matches[2]) AS INTEGER) AS price_in_birr,
    media_path,
    CASE
        WHEN phone_numbers IS NOT NULL AND phone_numbers != '' THEN phone_numbers
        ELSE NULL
    END AS contact_phone_numbers,
    cleaned_message AS message -- ADD THIS LINE to output the 'message' column
FROM product_price_extracted
WHERE matches IS NOT NULL
AND rn = 1
AND TRIM(matches[1]) <> ''
AND TRIM(matches[1]) <> TRIM(matches[2])
ORDER BY message_id