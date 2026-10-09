select
    o.order_id,
    o.calculated_total_amount,
    sum(i.line_amount) as items_total
from {{ ref('fct_orders') }} as o
inner join {{ ref('fct_order_items') }} as i on i.order_id = o.order_id
group by o.order_id, o.calculated_total_amount
having o.calculated_total_amount <> sum(i.line_amount)