select
    product_id,
    product_name,
    category,
    price,
    stock_quantity
from {{ ref('stg_products') }}