
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel_username
from "postgres"."public"."transformed_channel"
where channel_username is null



  
  
      
    ) dbt_internal_test