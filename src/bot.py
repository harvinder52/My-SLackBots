import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import re
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.')  /  '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app )
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id'] 

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    user = event.get('user')
    if BOT_ID != user_id:
       
       link1 = '<https://media.giphy.com/media/dkGhBWE3SyzXW/giphy.gif|Hell YEAH!>'
       link2 = '< https://media.giphy.com/media/3o7abGQa0aRJUurpII/giphy.gif|Great Work!>'
       string = " bots";
       if string in text:
         d = re.search('([\d,]*)([\D]*)(bots)',text)
         d1= re.search('(bots)([\d,]*)([\D]*)',text)
         noOfBots = (d.group(1))
         if (noOfBots ==""):
           noOfBots="0";  
           client.chat_postMessage(channel = channel_id , text=link1+" Keep finding those pesky bots")
         else:
           client.chat_postMessage(channel = channel_id , text="congratulations you found "+noOfBots+" bots "+link2)

       
         



if __name__ == "__main__" :
    app.run(debug=True)
    
