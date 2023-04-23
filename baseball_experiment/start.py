import os
import openai

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

#This will be an experment to see about using openai to generating stats for baseball players.

prompt = ' Give me a list of 10 former toronto bluejays players . <ul>'

def query_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["</ul>"]
    )
    return response


def format_results(response):
    results = response['choices'][0]['text']
    results = '<ul>' + results + '</ul>'
    return results

results = query_openai(prompt)
print(format_results(results))
