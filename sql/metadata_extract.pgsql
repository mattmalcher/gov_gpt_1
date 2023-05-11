
SELECT 
    trim('"' FROM link::text), 
    trim('"' FROM updated_at::text)::timestamp
FROM (
    SELECT DISTINCT
        cmetadata::jsonb->'link' AS link,
        cmetadata::jsonb->'updated_at' AS updated_at
    FROM
        embed_schema.langchain_pg_embedding
    ) a;
