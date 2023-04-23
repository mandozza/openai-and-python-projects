import os
import openai

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

num_questions = 5
num_possible_answers = 4

# Prompt the user for the topic they want to create a quiz on.
def prompt_input():
    nlp_text = input("What topic would you like to create a quiz on: ")
    return nlp_text

# Query the openai api with the prompt.
def query_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=300
    )
    return response

# Create the prompt for the user to create a quiz.
def create_test_prompt(topic, num_questions, num_possible_answers):
    prompt = f"Create a multiple choice quiz on the topic of {topic }. Consisting of {num_questions} questions "\
            +f"Each question should have {num_possible_answers} options for each question. There should only be 1 correct answer"\
            +f"Each question should have a correct answer using the starting string 'Correct Answer:' "
    return prompt


# Create a student view of the quiz.
def create_student_view(quiz, num_questions):
    student_view = {1: ''}
    question_number = 1
    for line in quiz.split("\n"):
        if not line.startswith("Correct Answer:"):
            student_view[question_number] += line + "\n"
        else:
            if question_number <= num_questions:
                question_number += 1
                student_view[question_number] = ''
    return student_view

def extract_answers(quiz, numofquestions):
    answers = {1: ''}
    question_number = 1
    for line in quiz.split("\n"):
        if line.startswith("Correct Answer:"):
              answers[question_number]= line.replace("Correct Answer:", "")
              if question_number <= numofquestions:
                question_number += 1
                answers[question_number] = ''
    return answers


# start the script
topic = prompt_input()
prompt = create_test_prompt(topic, num_questions, num_possible_answers)
results = query_openai(prompt)
student_view = create_student_view(results['choices'][0]['text'], num_questions)
answers = extract_answers(results['choices'][0]['text'], num_questions)

for key in student_view:
  print(student_view[key])

for key in answers:
  print(answers[key])


