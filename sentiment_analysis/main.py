import openai
import praw
import os
from dotenv import load_dotenv

load_dotenv()
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_SECRET_KEY")
openai.api_key = os.getenv('OPENAI_SECRET_KEY')

reddit = praw.Reddit(client_id=reddit_client_id,client_secret=reddit_client_secret,user_agent='sentiment analysis test')

subreddit_stocks = reddit.subreddit('stocks')

def get_title_and_comments(subreddit="stocks", limit=6, num_comments=3, skip_first=2):
    subreddit = reddit.subreddit(subreddit)
    title_and_comments = {}
    for counter,post in enumerate(subreddit.hot(limit=limit)):
        if counter < skip_first:
            continue

        counter += (1-skip_first)

        title_and_comments[counter] = ""

        submission = reddit.submission(post.id)
        title = post.title

        title_and_comments[counter] += "Title: " + title + "\n\n"
        title_and_comments[counter] += "Comments: \n\n"

        comment_counter = 0

        for comment in submission.comments:
            if not comment.body == '[removed]' or comment.body == '[deleted]':
                title_and_comments[counter] += comment.body + "\n\n"
                comment_counter += 1
            if comment_counter == num_comments:
                break
    return title_and_comments

def create_prompt(title_and_comments):
    task = "Return the stock ticker or company name that is being discussed in the following title and comments and classify the sentiment as positive, negative or neutral.If no ticker or company is mentioned write' No company mentioned' \n\n"
    return task + title_and_comments

def query_openai(title_and_comments):
  for key, title_with_comments in title_and_comments.items():
      prompt = create_prompt(title_with_comments)
      response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=prompt,
          temperature=0,
          max_tokens=256,
          top_p=1.0,
      )
      print(title_with_comments)
      formatted_response = response['choices'][0]['text']
      print(f"Sentiment Report from Open AI: {formatted_response}")
      print("---------------------------------------------------")



title_and_comments = get_title_and_comments()
response = query_openai(title_and_comments)





