
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel_title
from "postgres"."public"."transformed_channel"
where channel_title is null



  
  
      
    ) dbt_internal_test