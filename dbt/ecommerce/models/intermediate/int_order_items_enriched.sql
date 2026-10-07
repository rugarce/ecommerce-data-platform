select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price as line_amount,
    o.customer_id,
    o.order_date,
    o.status as order_status,
    p.product_name,
    p.category
from {{ ref('stg_order_items') }} as oi
inner join {{ ref('stg_orders') }} as o
    on oi.order_id = o.order_id
inner join {{ ref('stg_products') }} as p
    on oi.product_id = p.product_id