import os
import openai
import inspect

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

def hello(name):
    print(f"Hello {name}")

def get_code(function_name):
    lines = inspect.getsource(function_name)
    return lines

def create_prompt(function_name):
    code = get_code(function_name)
    prompt = f"{code}\n A  high quality python docstring of the above Python function:\n \"\"\""
    return prompt

def query_openai(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1.0,
        stop=["\"\"\""]
    )
    return response

def merge_docstring_and_code(docstring, code):
    code_string = get_code(code)
    code_string = code_string.split("\n")
    code_string_start = code_string[0]
    code_string_end = code_string[1:]

    merged_function = code_string_start + '\n    """' + docstring + '    """' + '\n' + "\n".join(code_string_end)
    return merged_function

def get_docstring(response):
    docstring = response['choices'][0]['text']
    return docstring


prompt = create_prompt(hello)
response = query_openai(prompt)
docstring = get_docstring(response)
print(merge_docstring_and_code(docstring, hello))
