{#
  Pregunta: ¿qué días de la semana se vende más? ¿Pesa el fin de semana?
#}

select
    d.day_of_week,
    d.day_name,
    d.is_weekend,
    count(*) as completed_orders,
    sum(o.calculated_total_amount) as revenue
from {{ ref('fct_orders') }} as o
inner join {{ ref('dim_date') }} as d on o.order_date = d.date_day
where o.order_status = 'completed'
group by d.day_of_week, d.day_name, d.is_weekend
order by d.day_of_week