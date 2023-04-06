Playing around with large language models.

There is a lot of noise at the moment about LLMs and I want to build up a little bit of experience using them.

A common idea is providing a chatbot as an interface for a set of documents that represent an organisation's knowledge.

As a starting point, I have previously worked with the gov.uk search and content APIs. They are easy to use, public and they serve up a wide range of content that is interesting to ask questions of (gov.uk guidance).


# Context

Matt Upson (former GDS I think?) has built something similar here:
https://medium.com/mantisnlp/chatgpt-for-gov-uk-c6f232dae7d

It doesnt say how they have anchored responses to gov.uk, but I doubt they have fine tuned or re-trained an LLM.

The Bing blog has a few hints, talking about how their 'Prometheus' orchestrator brings together search and chatgpt.
https://blogs.bing.com/search-quality-insights/february-2023/Building-the-New-Bing


# Goal

Make a web app, where the user can ask a question about UK government related topics and get a response that is likely to be right.

# Approach

## Proposal
* get question from user
* take question and extract topic to use as search term
* hit gov.uk/search and get back related content
* structure the content into a prompt. In the context of {content}, please answer {user question}
* return answer to user.


## Sticking points

While it seems possible to extract the relevant topics from the questions, searching these on gov.uk seems really hit & miss. You get some content which is relevant, but it might be 1/5 documents.

If you were to then put the content of the 4/5 unrelated documents into the prompt I imagine it could be somewhat distracting for the LLM.

I expect that to get good results you need to do some extra steps to ensure the context you are filling the prompt up with is relevant.

## Alternatives

### Custom Search
* maybe you could create a custom google search for gov.uk 
    * https://developers.google.com/custom-search/v1/overview 
    * https://fogine.dev/blog/how-to-programmatically-get-google-search-results/ 

### Vector Similarity
* openai have an example of using a document library to answer questions, they preprocess the document library first and use vector similarity to identify relevant content

If you were to pick a big area, say Tax, how much content is there on gov.uk that you would need to generate embeddings for?

HMRC has 90k pages of content: 

```sh
curl -s "https://www.gov.uk/api/search.json?count=0&filter_any_organisations=hm-revenue-customs&fields=id,indexable_content" | jq '.total'
```

To get that content using the content API @ half the rate limit would be (90,000/5)/3600 = 5 hours, which is managable.

You could use a simple local model for embeddings rather than making calls to the openai embeddings API.

I think you would want to generate vector per paragraph or something.

# What about Local LLMs?

There has been a lot of progress in getting LLMs running inference locally with limited resources.

I can run 7B, 13B versions of LLaMA / Alpaca / gpt4all models locally using CPU, but I dont have a GPU (and one with enough VRAM is prohibitively expensive.)

The approach proposed requires quite long prompts - thousands of tokens, because it includes all the context from the search results.

I can get results on the order of 2-5 tokens per second, this means that processing the prompts takes too long (10s of minutes). This makes it hard to develop, iterate on and use the code with a local LLM.

As such, the approach for now will be to use the openAI APIs. They provide 5$ of free credit, and have the ability to set a hard limit, lets see how far we can get with a few quid!


# Extension Ideas

Things that have occured to me, but are distractions from doing an MVP:

* Validate / threshold search result relevants by generating vectors and checking for similarity to question?
