
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message
from "postgres"."public"."transformed_medical_product"
where message is null



  
  
      
    ) dbt_internal_test