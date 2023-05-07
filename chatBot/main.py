import os
import openai

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

class CreateBot:

    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.messages = [{'role': 'system', 'content':system_prompt}]

    def chat(self):
        print('Ask a question about any band! To end the chat type "END"')
        question = ''

        while question != "END":
            question = input("")
            print('/n')
            self.messages.append({'role': 'user', 'content': question})
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.messages)
            content = response['choices'][0]['message']['content']
            self.messages.append({'role': 'assistant', 'content': content})
            print(content)



music_tutor = CreateBot('You are an expert an modern music. You are helping to teach a history class about the history of music.')
music_tutor.chat()
