select
    payment_id,
    order_id,
    payment_date,
    payment_method,
    amount,
    status
from {{ ref('stg_payments') }}