
# Application - Semantic Search

I think we want to use sbert for asymmetric semantic search

from: https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search

> or asymmetric semantic search, you usually have a short query (like a question or some keywords) and you want to find a longer paragraph answering the query. An example would be a query like “What is Python” and you wand to find the paragraph “Python is an interpreted, high-level and general-purpose programming language. Python’s design philosophy …”. For asymmetric tasks, flipping the query and the entries in your corpus usually does not make sense.


# Similarity Measure

from: https://www.sbert.net/docs/pretrained-models/msmarco-v3.html#performance

> Models tuned for cosine-similarity will prefer the retrieval of shorter passages, while models for dot-product will prefer the retrieval of longer passages. Depending on your task, you might prefer the one or the other type of model.


# Which Model?

There is a comparison table at: https://www.sbert.net/docs/pretrained_models.html#model-overview

This has two columns we are very interested in - speed & semantic search performance.

As of time of writing the `multi-qa-MiniLM-L6-cos-v1` model is ranked 4th in accuracy for semantic search applications, but is significantly faster (3x or more) than the top 3 so seems like a good place to start.


This model outputs embeddings vectors of length 385 (i.e. 0:384) 