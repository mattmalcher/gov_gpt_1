with unique_content as (
    SELECT 
        DISTINCT ON (content) * 
    FROM pages 
    )
select 
    link,
    format,
    trim(regexp_replace(content, '\s{2,}', ' ', 'g')) as content, -- avoids annoying manual pages with hundreds of repeated spaces filling the prompt
    updated_at,
    public_timestamp
from unique_content
