select
    oi.order_item_id
from {{ ref('stg_order_items') }} as oi
left join {{ ref('stg_orders') }} as o
    on oi.order_id = o.order_id
where o.order_id is null