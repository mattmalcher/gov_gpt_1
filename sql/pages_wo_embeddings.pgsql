WITH 
embeddings AS (
    SELECT 
        trim('"' FROM link::text) AS link, 
        trim('"' FROM updated_at::text)::timestamp AS updated_at
    FROM (
    SELECT DISTINCT
        cmetadata::jsonb->'link' AS link,
        cmetadata::jsonb->'updated_at' AS updated_at
    FROM
        embed_schema.langchain_pg_embedding
    ) a
),
unique_content AS (
    SELECT 
        DISTINCT ON (content) * 
    FROM pages 
)
SELECT 
    p.*
FROM 
    unique_content p
LEFT JOIN embeddings e ON p.link = e.link
WHERE 
    e.updated_at is NULL OR 
    p.updated_at < e.updated_at
LIMIT 1000