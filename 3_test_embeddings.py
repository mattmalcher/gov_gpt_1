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
        "k": 5, 
        "similarity_score_threshold":0.99
        })

question = questions[2]["question"]


sep = "---------------------\n"

print(f"{question}{sep}")

docs = retriever.get_relevant_documents(question)

for count, doc in enumerate(docs):
    print(f"{sep}Document {count + 1}\n"
          f"Source: {doc.metadata['source']}\n"
          f"Length: {len(doc.page_content)}\n"
          f"{sep}{doc.page_content}")

"done"