{#
  Pregunta: ¿cuánto se ha cobrado por método de pago y qué porcentaje de pagos se completa?
#}

select
    payment_method,
    count(*) as payments,
    count(*) filter (where status = 'completed') as completed_payments,
    round(100.0 * count(*) filter (where status = 'completed') / count(*), 1) as completion_rate_pct,
    sum(amount) filter (where status = 'completed') as collected_amount,
    sum(amount) filter (where status <> 'completed') as outstanding_amount
from {{ ref('fct_payments') }}
group by payment_method
order by collected_amount desc nulls last