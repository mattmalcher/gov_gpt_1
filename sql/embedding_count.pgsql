SELECT 
    COUNT( DISTINCT cmetadata::jsonb->'link' ) AS n_links
FROM
    embed_schema.langchain_pg_embedding
  