import openai

import govgpt.text_proc

# list models
__models__ = openai.Model.list()

__model_id__ = [model.id for model in __models__.data]


def text_from_response(response):

    text = response.choices[0].text

    cleantext = govgpt.text_proc.clean_response(text)

    return cleantext


def summarise_question(question, model="text-curie-001"):
    # https://platform.openai.com/docs/models/gpt-3

    if not model in __model_id__:
        raise ValueError(f'Invalid model: {model}. Accepted values are {__model_id__}.')

    
    response = openai.Completion.create(
        model=model,
        prompt= f"""Summarize the topics in the following question:
        #####
        {question}
        #####
        The three most important topics in this question are:
        """,
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response


