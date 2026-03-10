WITH source AS (
    SELECT
        Date        AS price_date,
        ticker,
        Open        AS open_price,
        High        AS high_price,
        Low         AS low_price,
        Close       AS close_price,
        Volume      AS volume,
        extracted_at
    FROM {{ source('raw', 'stock_prices') }}
)

SELECT * FROM source