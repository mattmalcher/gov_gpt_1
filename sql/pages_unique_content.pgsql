with unique_content as (
    SELECT 
        DISTINCT ON (content) * 
    FROM pages 
    )
select * from unique_content
