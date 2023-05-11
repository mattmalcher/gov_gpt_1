import logging
import logging.config

from langchain.vectorstores.pgvector import PGVector, DistanceStrategy
from govgpt.embeddings import embeddings
from govgpt.db import conn_string

logging.config.fileConfig('logging_config.ini', disable_existing_loggers=True)
logger = logging.getLogger()

from dev.example_questions import questions

store = PGVector(
    connection_string = "postgresql://" + conn_string, 
    embedding_function = embeddings, 
    collection_name = "sample_1",
    distance_strategy = DistanceStrategy.COSINE
)

retriever = store.as_retriever(
    search_kwargs={
        "k": 10, 
        "similarity_score_threshold":0.7
        })

docs = retriever.get_relevant_documents(questions[0]["question"])

"done"