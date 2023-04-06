Playing around with large language models.

There is a lot of noise at the moment about LLMs and I want to build up a little bit of experience using them.

A common idea is providing a chatbot as an interface for a set of documents that represent an organisation's knowledge.

As a starting point, I have previously worked with the gov.uk search and content APIs. They are easy to use, public and they serve up a wide range of content that is interesting to ask questions of (gov.uk guidance).


# Context

Matt Upson (former GDS) has built something similar here:
https://medium.com/mantisnlp/chatgpt-for-gov-uk-c6f232dae7d

It doesnt say how they have anchored responses to gov.uk, but I doubt they have fine tuned or re-trained an LLM.

The Bing blog has a few hints 
https://blogs.bing.com/search-quality-insights/february-2023/Building-the-New-Bing



# Goal

Make a web app, where the user can ask a question about UK government related topics and get a response that is likely to be right.

# Approach

* get question from user
* take question and extract topic to use as search term
* hit gov.uk/search and get back related content
* structure the content into a prompt. In the context of {content}, please answer {user question}
* return answer to user.


# What about Local LLMs?

There has been a lot of progress in getting LLMs running inference locally with limited resources.

I can run 7B, 13B versions of LLaMA / Alpaca / gpt4all models locally using CPU, but I dont have a GPU (and one with enough VRAM is prohibitively expensive.)

The approach proposed requires quite long prompts - thousands of tokens, because it includes all the context from the search results.

I can get results on the order of 2-5 tokens per second, this means that processing the prompts takes too long (10s of minutes). This makes it hard to develop, iterate on and use the code with a local LLM.

As such, the approach for now will be to use the openAI APIs. They provide 5$ of free credit, and 


# OpenAI APIs

## Links
