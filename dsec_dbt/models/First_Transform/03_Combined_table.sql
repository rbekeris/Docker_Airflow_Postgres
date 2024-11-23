{{ config(
  materialized='table'
) }}

select
  refined_eurostat.date,
  refined_eurostat.commodity_name,
  refined_eurostat."DE - Hamburg - DEPSILO",
  refined_cot.pct_of_oi_noncomm_long_all

from {{ source('Eurostat', '02_Refined_Eurostat') }} refined_eurostat

left join  {{ source('CFTC', '01_Refined_COT_Report') }} refined_cot
on refined_eurostat.date = refined_cot.date


