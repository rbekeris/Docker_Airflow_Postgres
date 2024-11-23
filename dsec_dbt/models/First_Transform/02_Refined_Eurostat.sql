{{ config(
  materialized='table'
) }}

with raw_eurostat as (

    select raw_eurostat.*

    from {{ source('Eurostat', '07_Eurostat_Wheat_Prices') }} raw_eurostat
    
)

select
  raw_eurostat."Date to" as date,
  'WHEAT' as commodity_name,
  raw_eurostat."DE - Hamburg - DEPSILO"

from raw_eurostat

where raw_eurostat."DE - Hamburg - DEPSILO" is not null


