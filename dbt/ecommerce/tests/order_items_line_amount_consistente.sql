select
    order_item_id,
    quantity,
    unit_price,
    line_amount
from {{ ref('fct_order_items') }}
where line_amount <> quantity * unit_price