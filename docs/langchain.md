On the face of it, langchain looks like an ideal starting point. There is an example of Question Answering over documents here: https://python.langchain.com/en/latest/use_cases/question_answering.html


# Components

It has components for the things we want ... but, probably because its quite early days and its changing a lot it is not always obvious how to use these components, or if one that is directly relevant exists.

## [Document Loaders](https://python.langchain.com/en/latest/modules/indexes/document_loaders.html) 

These retun lists of [Document](https://github.com/hwchase17/langchain/blob/812e5f43f541ed8a20f6105f44ddb7e82d86abf2/langchain/schema.py#L269) objects. 

There is a really long list of these, but I cant see one for postgres! 

Could crib from the [DuckDB Loader](https://github.com/hwchase17/langchain/blob/812e5f43f541ed8a20f6105f44ddb7e82d86abf2/langchain/document_loaders/duckdb_loader.py#L7) or [BigQuery Loader](https://github.com/hwchase17/langchain/blob/812e5f43f541ed8a20f6105f44ddb7e82d86abf2/langchain/document_loaders/bigquery.py)

Also - these seem set up to load all the documents at once by appending them to a list, rather than returning a generator or something. So you would need to add your own logic to work through them in chunks?

I think you could make a loader like so that would be useful:

```py

class PGDBLoader(BaseLoader):
    """Loads a query result from Postgres into a list of documents.

    query could be either something that returns all docs,
    or just those without existing embeddings,
    or those without up to date embeddings.

    """

    def __init__(
        self,
        query: str,
        database: str = ":memory:",
        read_only: bool = False,
        page_content_columns: Optional[List[str]] = None,
        metadata_columns: Optional[List[str]] = None,
        max_docs: int = 10e3
    ):
        ...

    return docs

```

## [Text Splitters](https://python.langchain.com/en/latest/modules/indexes/text_splitters.html)

To split them up text in chunks that fit into the model you are using. 
The model we are using to generate embeddings is the SBERT stuff.

The example using the [huggingface length function](https://python.langchain.com/en/latest/modules/indexes/text_splitters/examples/huggingface_length_function.html) shows using the GPT2 tokenizer, but I think we could probably use the sbert one by doing something like:

```py
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("models/multi-qa-MiniLM-L6-cos-v1/")
```

From there we should be able to use the langchain stuff directly:

```py
text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer, 
    chunk_size=100, 
    chunk_overlap=0
    )
texts = text_splitter.split_text(state_of_the_union)
```


## [Embeddings](https://python.langchain.com/en/latest/modules/models/text_embedding.html)

Langchain has support for sentence transformers embeddings: https://python.langchain.com/en/latest/modules/models/text_embedding/examples/sentence_transformers.html

You can generate an 'embeddings' object that can be passed to VectorIndex as follows:

```py
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="models/multi-qa-MiniLM-L6-cos-v1/")
```


## [Vectorstores](https://python.langchain.com/en/latest/modules/indexes/vectorstores.html)
    
The vectorstores are different options of where to store and search through your embeddings.

There is a [PGVector](https://python.langchain.com/en/latest/modules/indexes/vectorstores/examples/pgvector.html) example.


The PGVector class has a [`PGVector.add_texts()`](https://github.com/hwchase17/langchain/blob/812e5f43f541ed8a20f6105f44ddb7e82d86abf2/langchain/vectorstores/pgvector.py#L195) method that looks like what we want.

The example just shows how to 

    * comments in this issue demonstrates how you might re-load an existing PGVector store https://github.com/hwchase17/langchain/issues/3191


```py

store = PGVector(
    connection_string=connection_string, 
    embedding_function=embedding, 
    collection_name=collection_name,
    distance_strategy=DistanceStrategy.COSINE
)

```

Vectorstores are classes with methods for creating, updating and searching using the index.


## [Retrievers](https://python.langchain.com/en/latest/modules/indexes/retrievers.html)

A retriever is a generic way to get text relevant to a search term. 

You can have retrievers that are not simply a wrapper around a VectorStore, for example using Azure Cognitive Services or ElasticSearch.

In our case though, the [Vectorstore retriever](https://python.langchain.com/en/latest/modules/indexes/retrievers/examples/vectorstore-retriever.html) is probably what we want.

Following on from the example in Vectorstores thats as easy as:

```py

retriever = store.as_retriever()

```

We could (after getting the other stuff working) write a retriever to augment the results from the Vectorstore with the surrounding text from the relevant gov.uk page, rather than just the chunk the embedding was based on.
