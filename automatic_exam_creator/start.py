import os
import openai

openai.api_key = os.getenv('OPENAI_SECRET_KEY')

num_questions = 4
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
        temperature=0,
        max_tokens=350
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

#pulls out the answers from the quiz.
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

# runs the test and gets answers.
def take_test(student_view):
    student_answers = {}
    for question, question_text in student_view.items():
        if(question_text == ''):
            continue
        print(question_text)
        student_answers[question] = input("Enter your answer: ")
    return student_answers

def grade_test(student_answers, answers):
    correct = 0
    for question, answer in student_answers.items():
        if answer.upper() == answers[question][1]:
            correct += 1
    grade = 100 * correct / len(student_answers)
    return f"You got {correct} out of {len(student_answers)} questions correct. Your grade is {grade}%"


# start the script
topic = prompt_input()
prompt = create_test_prompt(topic, num_questions, num_possible_answers)
results = query_openai(prompt)
student_view = create_student_view(results['choices'][0]['text'], num_questions)
answers = extract_answers(results['choices'][0]['text'], num_questions)
student_answers = take_test(student_view)
print(grade_test(student_answers, answers))


