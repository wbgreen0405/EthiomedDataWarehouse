
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select image_path
from "postgres"."public"."transformed_product_images"
where image_path is null



  
  
      
    ) dbt_internal_test