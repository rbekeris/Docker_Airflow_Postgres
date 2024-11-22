{{ config(
  materialized='table'
) }}

with raw_cot as (

    select raw_cot.*

    from {{ source('CFTC', '05_COT_Legacy_Combined_Report') }} raw_cot
    
)

select
  raw_cot.report_date_as_yyyy_mm_dd as date,

  raw_cot.commodity_name as commodity_name,
  raw_cot.pct_of_oi_noncomm_long_all,
  raw_cot.pct_of_oi_noncomm_short_all

from raw_cot

WHERE raw_cot.commodity_name = 'WHEAT'


