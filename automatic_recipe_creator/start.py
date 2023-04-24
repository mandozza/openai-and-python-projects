import os
import openai
import requests
import shutil
import re

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

# Query the openai api with the prompt.
def query_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=512
    )
    return response

#### query openai Dall-E for image.
def query_openai_dalle(prompt):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size='1024x1024',
    )
    return response

def dalle2_prompt(recipe_title):
    prompt = f"{recipe_title}, professional food photography, 15mm, studio lighting, in the style of Jackie Alpers, food photographer."
    return prompt

def create_dish_prompt(list_of_ingredients):
    core_ingredients = ['salt', 'pepper', 'vegetable oil', 'flour', 'bread', 'cheese', 'egg']
    prompt = f"Create a detailed recipe based on only the following ingredients: {', '.join(list_of_ingredients)}, {', '.join(core_ingredients)}.\n"\
            +f"Additionaly, assign a title starting with 'Recipe Title: ' to this recipe."
    return prompt

def extract_title(recipe):
    title = ''
    for line in recipe.split("\n"):
        if line.startswith("Recipe Title:"):
            title = line.replace("Recipe Title:", "")
            title = title.strip()
    return title


def save_recipe_image(recipe_image_url,file_name):
    image_res = requests.get(recipe_image_url, stream=True)
    if image_res.status_code == 200:
        with open(file_name, 'wb') as f:
          shutil.copyfileobj(image_res.raw, f)
    else:
        print("Couldn't save image")
    return image_res.status_code


def url_friendly_text(file_name):
    file_name = file_name.lower()
    file_name = re.sub(r'\s+', '_', file_name)
    file_name = '{:06d}_{}'.format(123456, file_name)
    return file_name

prompt = create_dish_prompt(['noodles', 'shirmp', 'garlic', 'onion', 'tomato', 'chicken', 'beef', 'pork', 'carrot', 'potato', 'cabbage', 'broccoli', 'mushroom', 'bell pepper', 'corn', 'green beans', 'peas', 'rice', 'egg', 'milk', 'butter', 'sugar', 'salt', 'pepper', 'vegetable oil', 'flour', 'bread', 'cheese', 'egg'])
result = query_openai(prompt)
result_text= result['choices'][0]['text']
recipe_title = extract_title(result_text)
result_recipe_image = query_openai_dalle(dalle2_prompt(recipe_title))
recipe_image_url = result_recipe_image['data'][0]['url']
save_recipe_image(recipe_image_url, url_friendly_text(recipe_title) + '.jpg')

print(recipe_title)
print(result_text)
print(recipe_image_url)
