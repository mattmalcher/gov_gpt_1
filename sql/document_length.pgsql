-- https://tapoueh.org/blog/2014/02/postgresql-aggregates-and-histograms/

with len_stats as (
    select min(length(document)) as min,
           max(length(document)) as max
      from embed_schema.langchain_pg_embedding
),
histogram as (
   select width_bucket(length(document), min, max, 50) as bucket,
          int4range(min(length(document)), max(length(document)), '[]') as range,
          count(*) as freq
     from embed_schema.langchain_pg_embedding, len_stats
 group by bucket
 order by bucket
)
 select bucket, range, freq,
        repeat('■',
               (   freq::float
                 / max(freq) over()
                 * 30
               )::int
        ) as bar
   from histogram;