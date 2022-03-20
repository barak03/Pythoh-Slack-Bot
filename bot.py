import slack
import os
from dotenv import load_dotenv
import dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
load_dotenv()

app = Flask(__name__)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/webhooks/slack/webhook', app)
twitter_token = os.environ['TWITTER_TOKEN']
twitter_secret = os.environ['TWITTER_SECRET']
twitter_brarer = os.environ['TWITTER_BRARER_TOKEN']
last_tweet_time_id = int(os.environ['LAST_TWEET_ID'])
BOT_ID = client.api_call("auth.test")['user_id']
headers = {"Authorization": "Bearer {0}".format(twitter_brarer)}
param = {'tweet.fields': 'created_at'}

def get_tweets():
    return_str = ''
    twitter_pages = {"Python Weekly": 373620985, "Real Python" : 745911914, "Full Stack Python" : 2996502625}
    for key, value in twitter_pages.items():
        result = requests.get(url = "https://api.twitter.com/2/users/{0}/tweets".format(value), params = param, headers = headers)
        data = result.json()
        last_tweet = data['data'][0]
        now_time = datetime.now()
        tweeet_time = datetime.fromisoformat(last_tweet['created_at'].replace("T", " ").replace("Z", ""))
        if (now_time.hour - tweeet_time.hour <= 1) and now_time.day == tweeet_time.day and tweeet_time.month == now_time.month:
            return_str = return_str + key + ": " + last_tweet['text'] + os.linesep
    
    if len(return_str) < 1:
        return_str = "There is no new content"
    return return_str

@slack_event_adapter.on('message')
def message(payload):
    print("im inside ")
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if text.lower() == "now":
        client.chat_meMessage(channel=channel_id, text=str(datetime.now().strftime(r"%m/%d/%Y, %H:%M:%S")))
    elif text.lower() == "new-content":
        last_tweets = get_tweets()
        client.chat_meMessage(channel=channel_id, text=last_tweets)

def check_new_tweets():
    global param
    global headers
    global last_tweet_time_id
    dotenv_path = "./.env"
    user_id = 729724789603061760
    result = requests.get(url = "https://api.twitter.com/2/users/{0}/tweets".format(user_id), params = param, headers = headers)
    data = result.json()
    last_tweet = data['data'][0]
    if last_tweet_time_id != int(last_tweet['id']):
        dotenv.set_key(dotenv_path, "LAST_TWEET_ID", (last_tweet['id']))
        last_tweet_time_id = int(last_tweet['id'])
        client.chat_meMessage(channel='#content', text=last_tweet['text'])

sched = BackgroundScheduler(daemon=True)
sched.add_job(check_new_tweets,'interval',minutes=1)
sched.start()

if __name__ == "__main__":
    app.run(debug=True, port=8082, use_reloader=False)