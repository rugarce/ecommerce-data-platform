{#
  Pregunta: ¿qué categorías pesan más en los ingresos?
#}

select
    p.category,
    count(distinct i.order_id) as completed_orders,
    sum(i.quantity) as units_sold,
    sum(i.line_amount) as revenue,
    round(100.0 * sum(i.line_amount) / sum(sum(i.line_amount)) over (), 1) as pct_of_revenue
from {{ ref('fct_order_items') }} as i
inner join {{ ref('dim_product') }} as p on i.product_id = p.product_id
where i.order_status = 'completed'
group by p.category
order by revenue desc