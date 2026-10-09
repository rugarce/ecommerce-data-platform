select
    order_item_id,
    order_id,
    product_id,
    customer_id,
    order_date,
    order_status,
    quantity,
    unit_price,
    line_amount
from {{ ref('int_order_items_enriched') }}