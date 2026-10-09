{#
  Control: pedidos 'completed' sin pago completado o con importe distinto,
  y pedidos cancelados que tienen algun pago. Resultado esperado: 0 filas.
#}

select
    o.order_id,
    o.order_status,
    o.calculated_total_amount,
    p.payment_id,
    p.status as payment_status,
    p.amount as paid_amount
from {{ ref('fct_orders') }} as o
left join {{ ref('fct_payments') }} as p on p.order_id = o.order_id
where (
        o.order_status = 'completed'
        and (
            p.payment_id is null
            or p.status <> 'completed'
            or p.amount <> o.calculated_total_amount
        )
    )
    or (o.order_status = 'cancelled' and p.payment_id is not null)