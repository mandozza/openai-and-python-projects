import pandas as pd
import json

## This script converts the QA dataset into the format required by OpenAI's fine-tuning script
## The fine-tuning is recomended to do via the CLI.
## The comanand is: openai fine_tunes.create -t "file path to dataset goes here" -m babbage

qa_df = pd.read_csv("python_qa.csv")

questions, answers = qa_df['Body'], qa_df['Answer']

qa_openai_format = [ {"question": q, "answer": a} for q, a in zip(questions, answers) ]

dataset_size = 500

with open("example_training_data.json", "w") as f:
    for entry in qa_openai_format[:dataset_size]:
        f.write(json.dumps(entry) + "\n")
