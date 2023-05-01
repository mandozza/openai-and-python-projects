import os
import openai
import requests
import bs4


openai.api_key = os.getenv('OPENAI_SECRET_KEY')

country_newspapers = {"Spain" : ("https://www.elpais.com/", ".c_t"), "France" : ("https://www.lemonde.fr/", ".article__title-label")}

def get_headlines(url, tag):
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.text, 'html.parser')
    titles = soup.select(tag)[:3]
    headlines =''
    for title in titles:
        headlines += title.getText() + '\n'

    return headlines

def create_prompt():
    country = input("What country do you want to read the news from? ")

    try:
        url, tag = country_newspapers[country]
    except:
      print("Sorry, we don't support this country yet")
      return

    headlines = get_headlines(url, tag)

    prompt = "Detect the language of the following headlines below, then translate a summary of the headlines to English in a conversational tone. \n\n" + headlines + "\n\nLanguage: \nEnglish: \nSummary: \n\n\n\n"

    return prompt

def query_openai(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=1.0
    )
    return response

def display_response(response):
    translation_string = response['choices'][0]['text']
    print(translation_string)

prompt = create_prompt()
response = query_openai(prompt)
display_response(response)
