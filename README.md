# Pythoh-Slack-Bot

This project is a basic Slack bot, that posts a messages to a channel called "content" from Twitter.<br/>
The bot uses REST API to accses Twitter and python library for salck to send slack massages.<br/>
When a memmber of the slack group sends a massage with the content "now" the bot will response with the current time. <br/>
When a memmber of the slack group sends a massage with the content "new-content", the bot pulls new tweets (new tweets are considered as all tweets from last hour) from the following pages:
- Python Weekly
- Real Python
- Full Stack Python

The bot has the ability to check for new tweets from my specific page, and post the new tweets automatically to the content channel.<br/>
