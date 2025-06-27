
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel_id
from "postgres"."public"."transformed_product"
where channel_id is null



  
  
      
    ) dbt_internal_test