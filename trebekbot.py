import requests
import tweepy
import time

# This function sends out a http request to jArchive for a random question
def send_question_query():
    # This is the url for the jArchive API
    url = "http://jservice.io/api/random"
    # This is the http request
    response = requests.get(url)
    # This returns the response as a json object

    # Now, extract the question, answer, category, and value from the json object
    # The json object is a list of dictionaries, so we need to extract the first dictionary

    question = response.json()[0]['question']
    answer = response.json()[0]['answer']
    category = response.json()[0]['category']['title']
    value = response.json()[0]['value']
    date = response.json()[0]['airdate']

    return question, answer, category, value, date

# Reads the question and answer
def state_question(question, answer, category, value, date):
    # format the date to be "Month of Year" where month is spelled out
    date = time.strftime('%B', time.strptime(date[:10], '%Y-%m-%d')) + " of " + time.strftime('%Y', time.strptime(date[:10], '%Y-%m-%d'))

    # Make the category all caps
    category = category.upper()

    question = "This episode aired in " + str(date) + ".\n\nFor " + str(value) + " dollars, the category is " + str(category) + ":\n\n" + str(question)

    # Search for the answer on wikipedia to get a link with more information about it
    answer = "The answer was:\n\nWhat is " + str(answer) + "?\n\nLearn more at https://en.wikipedia.org/wiki/" + str(answer).replace(" ", "_")

    return question, answer

# This takes in the twitter api to tweet a question, then tweets the answer 6 hours later
def tweet_question(question, answer, twitter_api):

    # Create a tweet
    twitter_api.update_status(question)

    # Wait 6 hours
    time.sleep(21600)

    # Create a tweet
    twitter_api.update_status(answer)


api_key = 'qjcyVowUu6W0blFWbay4rD6OL'
api_key_secret = 'nt2IVyRlaKrn5VP39BPPB0mymGVJJSIwWNFdBs5euacXv98Jtb'
access_token = '1268043010534760450-kBQmMMzlT2a9NfCWoykXEQWXkHxXOq'
access_token_secret = 'wrQP8zKvOGQrYCJCJSyKp0aATr5LZS4vrI3eToFCuaP5U'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
twitter_api = tweepy.API(auth)

while True:
    question, answer, category, value, date = send_question_query()
    question, answer = state_question(question, answer, category, value, date)
    tweet_question(question, answer, twitter_api)
