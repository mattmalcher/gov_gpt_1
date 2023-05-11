WITH dup_embeddings AS (
    SELECT
        count(*) as n_copies, 
        embedding
    FROM embed_schema.langchain_pg_embedding 
    GROUP BY embedding 
    HAVING COUNT(*) >1
    ORDER BY embedding
)
SELECT * FROM dup_embeddings d
LEFT JOIN embed_schema.langchain_pg_embedding e on e.embedding = d.embedding