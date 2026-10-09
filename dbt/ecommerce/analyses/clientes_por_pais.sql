{#
  Pregunta: ¿cómo se reparten clientes e ingresos por país?
  El left join mantiene los países cuyos clientes no han comprado nada.
#}

select
    c.country,
    count(distinct c.customer_id) as customers,
    count(distinct case when o.order_status = 'completed' then o.order_id end) as completed_orders,
    coalesce(sum(case when o.order_status = 'completed' then o.calculated_total_amount end), 0) as revenue,
    round(
        sum(case when o.order_status = 'completed' then o.calculated_total_amount end)
        / nullif(count(distinct case when o.order_status = 'completed' then o.order_id end), 0),
        2
    ) as avg_order_value
from {{ ref('dim_customer') }} as c
left join {{ ref('fct_orders') }} as o on o.customer_id = c.customer_id
group by c.country
order by revenue desc