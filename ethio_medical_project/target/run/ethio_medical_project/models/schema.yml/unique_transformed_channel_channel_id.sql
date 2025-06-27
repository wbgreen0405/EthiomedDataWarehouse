
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    channel_id as unique_field,
    count(*) as n_records

from "postgres"."public"."transformed_channel"
where channel_id is not null
group by channel_id
having count(*) > 1



  
  
      
    ) dbt_internal_test