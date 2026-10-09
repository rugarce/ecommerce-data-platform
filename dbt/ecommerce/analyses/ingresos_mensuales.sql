{#
  Pregunta: ¿cuánto facturamos cada mes y cómo evoluciona?
  Ingresos = suma de calculated_total_amount de pedidos 'completed'.
#}

with monthly as (
    select
        d.year,
        d.month,
        d.month_name,
        count(*) as completed_orders,
        sum(o.calculated_total_amount) as revenue
    from {{ ref('fct_orders') }} as o
    inner join {{ ref('dim_date') }} as d on o.order_date = d.date_day
    where o.order_status = 'completed'
    group by d.year, d.month, d.month_name
)

select
    year,
    month,
    month_name,
    completed_orders,
    revenue,
    lag(revenue) over (order by year, month) as previous_month_revenue,
    round(
        100.0 * (revenue - lag(revenue) over (order by year, month))
        / nullif(lag(revenue) over (order by year, month), 0),
        1
    ) as revenue_growth_pct
from monthly
order by year, month