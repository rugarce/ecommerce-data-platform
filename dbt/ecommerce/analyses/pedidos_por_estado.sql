{#
  Pregunta: ¿qué proporción de pedidos se completa, queda pendiente o se cancela?
#}

select
    order_status,
    count(*) as orders,
    round(100.0 * count(*) / sum(count(*)) over (), 1) as pct_of_orders,
    sum(calculated_total_amount) as total_amount
from {{ ref('fct_orders') }}
group by order_status
order by orders desc