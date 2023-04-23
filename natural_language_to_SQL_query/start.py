import os
import openai
import pandas as pd
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import text

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

## reading the data from the csv file
df = pd.read_csv('data/sales_data_sample.csv')

## creating a temporary database in memory
temp_db = create_engine('sqlite:///:memory:', echo=False)
data = df.to_sql('Sales', temp_db, if_exists='replace')

# Get the table definition and put it in a string.
def create_table_definition(df):
    prompt = """### sqllite SQL table, with its properties:
    #
    # Sales({})
    #
    """.format(",".join(str(col) for col in df.columns))
    return prompt

# Prompt the user for input for what they want to query./
def prompt_input():
    nlp_text =input("Enter the info you want: ")
    return nlp_text

# Combine the table definition with the user input to create a prompt.
def combine_prompts(df, query_prompt):
    definition = create_table_definition(df)
    query_init_string = f"### A query to answer: {query_prompt}\nSELECT"
    return definition + query_init_string

nlp_text = prompt_input()
generated_prompt = combine_prompts(df, nlp_text)

### pass the prompt to the GPT-3 model.
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=generated_prompt,
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["#", ";"]
)

# Handle the response from the GPT-3 model and create a sql query.
def handle_response(response):
    query = response['choices'][0]['text']
    query = "SELECT" + query
    return query

# Run the query against the temporary database.
def run_query(query):
    with temp_db.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()

# Call handle_response to get query string.
query = handle_response(response)
# Call run_query to get the result of the query.
result = run_query(query)
# Print the result.
print(result)



