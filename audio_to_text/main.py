import os
import openai

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

audio_file = open('Warren+Buffett+On+Exposing+Business+Frauds+And+Deception.mp3', 'rb')
transcribe = openai.Audio.transcribe("whisper-1", audio_file)

print(transcribe['text'])

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': 'You are good at creating bullet point summaries and have knowledge of Warren Buffett'},
        {'role': 'user', 'content': f"Summarize the following in bullet point form: \n{transcribe['text']}"}
    ]
)

print(response['choices'][0]['message']['content'])
