import openai
import os

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Give me two reasons to learn OpenAI API with Python",
    max_tokens=300)
print(response)

print(response['choices'][0]['text'])
