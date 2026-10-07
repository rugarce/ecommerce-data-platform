select
    order_id,
    customer_id,
    order_date,
    order_status,
    sum(line_amount) as calculated_total_amount,
    count(distinct product_id) as distinct_products,
    sum(quantity) as total_items
from {{ ref('int_order_items_enriched') }}
group by
    order_id,
    customer_id,
    order_date,
    order_status