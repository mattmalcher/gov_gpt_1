SELECT 
    COUNT( DISTINCT cmetadata::jsonb->'link' ) AS n_links,
    COUNT(embedding) as n_embeddings
FROM
    embed_schema.langchain_pg_embedding
  