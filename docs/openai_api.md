# OpenAI APIs

There is a python wrapper: https://github.com/openai/openai-python



## Links

API reference pages:
* https://platform.openai.com/docs/api-reference/completions/create

Available models and how to use them:
* https://platform.openai.com/docs/models
* https://platform.openai.com/examples


Figuring out how much you will spend & setting limits:
* https://openai.com/pricing
* https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
* https://platform.openai.com/account/billing/limits



# Summarise Question Responses

## Question 1

```
Summarize the key topics in this question:

Hi everyone,
I currently have a stocks and shares LISA which I paid £4k into last tax year (2022/23) just ended. Now the new tax year is upon us, I know i can add another £4k. However i don’t want to invest this time and just want a simple Cash LISA for 2023/24, which i would need to open now, rather than adding another £4k to the S&S one.
I know you can pay into each type of ISA (so long as only one of each specific type in the tax year), subject to the £20k max, but would I be able to have multiple LISAs of different types open at once?
I don’t believe having the arrangement below is an issue when it comes to realising the funds and bonuses when I want to buy (i.e i can’t only use one of the LISAs for a <450k property), but happy to be told otherwise aswell! S&S LISA (2022/23) Cash LISA (2023/24)

Thanks!
```

### `davinci-003`

Attempt 1 nails it, can we use a cheaper model though?

> The key topics in this question are: stocks and shares LISA, Cash LISA, having multiple LISAs of different types open at once, and being able to use both LISAs for a property purchase.

### `text-curie-001`


Attempt 1 seems to not quite get the instruction, its providing an answer to the user question.

> You can have multiple LISAs open at once, as long as the total amount you invest in them does not exceed £20,000.

Attempt 2 seems to be the same, its answering not summarising the topics

>-You can have up to three different types of ISAs open at once, as long as they are of different types 
>-You can pay into an S&S Isa up to £20,000 in total during the tax year
>-You can't pay into an S&S Isa that has already been paid into during the tax year



## Question 2

Looking at the answer given by davinci-003 gave me an idea for some updates to the prompt structure that might help:

```
Summarize the key topics in the following question:
#####
Hi everyone,
I currently have a stocks and shares LISA which I paid £4k into last tax year (2022/23) just ended. Now the new tax year is upon us, I know i can add another £4k. However i don’t want to invest this time and just want a simple Cash LISA for 2023/24, which i would need to open now, rather than adding another £4k to the S&S one.
I know you can pay into each type of ISA (so long as only one of each specific type in the tax year), subject to the £20k max, but would I be able to have multiple LISAs of different types open at once?
I don’t believe having the arrangement below is an issue when it comes to realising the funds and bonuses when I want to buy (i.e i can’t only use one of the LISAs for a <450k property), but happy to be told otherwise aswell! S&S LISA (2022/23) Cash LISA (2023/24)

Thanks!
#####
The key topics covered in this question are:
```
### `text-curie-001`

Attempt 1 at answering this seems _much_ better:

```
-Can you have multiple LISAs open at once?
-What is the maximum you can invest in an LISA?
-Can you use an LISA to invest in a property worth less than £450,000?
```

Attempt 2 is good, but we are losing the fact this is a question about LISAs

```
-Can you have multiple accounts opened with the same provider that are all of different types of savings account (S&S, Cash, stocks and shares)?
-What are the restrictions on how much you can contribute to each type of account?
-When can you use the funds in the accounts?
```

Attempt 3 has kept LISAs but lost property

```
-Can you have multiple LISAs open at once?
-How much can you invest in each LISA?
-What is the maximum you can invest in each LISA?
```


### `text-babbage-001`

Attempt 1 - not quite there but includes property, LISA and other search terms that would be useful

```
-How much can an individual pay into an ISA each year?
-Can an individual have multiple LISAs of the same type open at the same time?
-If an individual wants to buy a property with a LISA, what is the maximum amount they can pay into the ISA?
```

Attempt 2 - misses the mark because its not about retirement in this case, but property

```
-How much money can someone retire with in a given year?
-How much money can someone save in a given year?
-Are there any restrictions on how many retirement savings can be held at once?
-Does anyone have any advice about using a LISA for buying a home?
```