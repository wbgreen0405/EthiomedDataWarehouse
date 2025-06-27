
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select contact_phone_number
from "postgres"."public"."transformed_contact_number"
where contact_phone_number is null



  
  
      
    ) dbt_internal_test