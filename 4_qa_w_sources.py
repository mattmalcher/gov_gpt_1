import logging
import logging.config

logging.config.fileConfig('logging_config.ini', disable_existing_loggers=True)
logger = logging.getLogger()

from langchain.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain.llms import OpenAI
#from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains import RetrievalQA

from govgpt.embeddings import embeddings
from govgpt.db import conn_string
from govgpt.openai_api import openai_api_key

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
        "similarity_score_threshold":0.7
        })

# for sources to work need metadata key called 'source'
#qa = RetrievalQAWithSourcesChain.from_chain_type(
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(
       # model_name="text-curie-001", 
        model_name="text-davinci-003", 
        openai_api_key = openai_api_key
    ), 
    chain_type="stuff", 
    retriever=retriever,
    verbose=True
    )

question = questions[0]["question"]

output = qa(question)

print(
    f"\n{'-'*70}\nQuestion:\n{question}"
    f"\nOutput:\n{output['result']}"
    )

"done"
