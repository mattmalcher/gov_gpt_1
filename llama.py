from pyllamacpp.model import Model
from govgpt import search


model = Model(ggml_model='/home/matt/repos/misc/llama.cpp/models/gpt4all-7b/gpt4all-lora-quantized-new.bin', n_ctx=4096)

def new_text_callback(text: str):
    print(text, end="")

question = "I think I need to pay air passenguer duty, is that true?"

topic_prompt = f"""
what is the key topic of the following question?
---
{question}
---
TOPIC:
"""

resp = model.generate(topic_prompt, n_predict=55, new_text_callback=new_text_callback)

search_string = resp[len(topic_prompt)+1:]


print(search_string)

content = search.search_gov_uk_with_content(search_string)

prompt_context = " ".join([c[:1000] for c in content[:3]])


context_q_prompt = f"""
Consider the below context

##########
CONTEXT: 
{prompt_context}

###########
In this context answer the question

############
QUESTION: {question}
ANSWER:"""

print(context_q_prompt)
print(len(context_q_prompt))

resp_2 = model.generate(context_q_prompt,    n_predict=500, new_text_callback=new_text_callback)

answer = resp_2[len(context_q_prompt)+1:]
