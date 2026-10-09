{#
  Pregunta: ¿qué productos generan más ingresos?
  Ingresos = line_amount de líneas de pedidos 'completed'.
#}

select
    p.product_id,
    p.product_name,
    p.category,
    sum(i.quantity) as units_sold,
    sum(i.line_amount) as revenue,
    round(100.0 * sum(i.line_amount) / sum(sum(i.line_amount)) over (), 1) as pct_of_revenue,
    rank() over (order by sum(i.line_amount) desc) as revenue_rank
from {{ ref('fct_order_items') }} as i
inner join {{ ref('dim_product') }} as p on i.product_id = p.product_id
where i.order_status = 'completed'
group by p.product_id, p.product_name, p.category
order by revenue_rank