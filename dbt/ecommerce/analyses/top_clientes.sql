{#
  Pregunta: ¿quiénes son nuestros 10 mejores clientes y cuánto pesan en el total?
  No usar LIMIT: dbt show añade el suyo. Se filtra por ranking (incluye empates).
#}

with customer_revenue as (
    select
        c.customer_id,
        c.first_name || ' ' || c.last_name as customer_name,
        c.country,
        count(*) as completed_orders,
        sum(o.calculated_total_amount) as revenue
    from {{ ref('fct_orders') }} as o
    inner join {{ ref('dim_customer') }} as c on o.customer_id = c.customer_id
    where o.order_status = 'completed'
    group by c.customer_id, c.first_name, c.last_name, c.country
),

ranked as (
    select
        rank() over (order by revenue desc) as revenue_rank,
        customer_id,
        customer_name,
        country,
        completed_orders,
        revenue,
        round(100.0 * revenue / sum(revenue) over (), 1) as pct_of_total_revenue
    from customer_revenue
)

select * from ranked
where revenue_rank <= 10
order by revenue_rank