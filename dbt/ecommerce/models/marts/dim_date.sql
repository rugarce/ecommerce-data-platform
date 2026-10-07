with date_spine as (

    select
        generate_series(
            '2025-01-01'::date,
            '2025-12-31'::date,
            interval '1 day'
        )::date as date_day

)

select
    date_day,
    extract(year from date_day)::integer as year,
    extract(quarter from date_day)::integer as quarter,
    extract(month from date_day)::integer as month,
    to_char(date_day, 'Month') as month_name,
    extract(day from date_day)::integer as day,
    extract(isodow from date_day)::integer as day_of_week,
    to_char(date_day, 'Day') as day_name,
    case
        when extract(isodow from date_day) in (6, 7) then true
        else false
    end as is_weekend
from date_spine