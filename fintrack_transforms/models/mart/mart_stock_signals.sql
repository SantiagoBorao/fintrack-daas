WITH base AS (
    SELECT
        price_date,
        ticker,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    FROM {{ ref('stg_stock_prices') }}
)
,with_moving_averages AS (
    SELECT
        *,
        AVG(close_price) OVER (
            PARTITION BY ticker
            ORDER BY price_date
            ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
        ) AS sma_50,

        AVG(close_price) OVER (
            PARTITION BY ticker
            ORDER BY price_date
            ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
        ) AS sma_200,

        AVG(volume) OVER (
            PARTITION BY ticker
            ORDER BY price_date
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ) AS avg_volume_10d

    FROM base
)
,with_volume_alerts AS (
    SELECT
        *,
        CASE
            WHEN volume > avg_volume_10d * 3 THEN TRUE
            ELSE FALSE
        END AS flag_volume_alert,

        CASE
            WHEN sma_50 > sma_200 THEN 'GOLDEN_CROSS'
            WHEN sma_50 < sma_200 THEN 'DEATH_CROSS'
            ELSE 'NEUTRAL'
        END AS cross_signal

    FROM with_moving_averages
)

SELECT * FROM with_volume_alerts