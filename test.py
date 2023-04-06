from dev import example_questions

from govgpt import openai_api
from govgpt import gov_search


question = example_questions.questions[3]["question"]

print(f"\nQuestion:---------\n{question}\n")

resp = openai_api.summarise_question(question, model = "text-davinci-003")

summary_question = openai_api.text_from_response(resp)

print(f"\nSummary Question ---------\n{summary_question}\n")

content = gov_search.search_gov_uk_with_content(summary_question)

content
