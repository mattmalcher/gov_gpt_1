# Why vector database

https://learn.microsoft.com/en-us/semantic-kernel/concepts-ai/vectordb#use-cases-for-vector-databases


# Which vector database?

Some relevant questions:

* is it open source
* can I run it locally easily
* can I store other data in it as well, or do I need multiple databases
* do ORM's support it?
* how crazy would it be to get it running in a corporate environment?
* are there any gamechanger features or algorithims I require past cosine similarity?
* does langchain support it?


# Options

## Pinecone
Looks like managed service only?

## pgvector

Supported by AWS RDS

FOSS

Supported by langchain - https://python.langchain.com/en/latest/modules/indexes/vectorstores/examples/pgvector.html

Can be run locally and could serve my other needs too.



# Refs
https://towardsdatascience.com/milvus-pinecone-vespa-weaviate-vald-gsi-what-unites-these-buzz-words-and-what-makes-each-9c65a3bd0696?gi=6bc319edab81


https://news.ycombinator.com/item?id=35308551

List of langchain vector stores
https://python.langchain.com/en/latest/modules/indexes/vectorstores.html

