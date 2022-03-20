# Pythoh-Slack-Bot

This project is a basic Slack bot, that posts messages to a channel called "content" from Twitter.<br/>
The bot uses REST API to access Twitter and python library for slack to send slack messages.<br/>
When a member of the slack group sends a message with the content "now" the bot will respond with the current time. <br/>
When a member of the slack group sends a message with the content "new-content", the bot pulls new tweets (new tweets are considered as all tweets from the last hour) from the following pages:
- Python Weekly
- Real Python
- Full Stack Python

The bot has the ability to check for new tweets from my specific page every 1-minute using BackgroundScheduler, and post the new tweets automatically to the content channel.<br/>
All the neccesry variables are loaded from .env file.<br/>


# massage examples

![new-content massage example](https://github.com/barak03/Pythoh-Slack-Bot/blob/main/Images/new-content.png)

![now massage example](https://github.com/barak03/Pythoh-Slack-Bot/blob/main/Images/now.png)
