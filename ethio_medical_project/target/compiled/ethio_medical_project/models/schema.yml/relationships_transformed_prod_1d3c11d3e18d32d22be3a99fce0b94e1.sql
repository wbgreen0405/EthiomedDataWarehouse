
    
    

with child as (
    select product_id as from_field
    from "postgres"."public"."transformed_product_images"
    where product_id is not null
),

parent as (
    select product_id as to_field
    from "postgres"."public"."transformed_medical_product"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


