import slack
import os
import requests, json
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

token=os.environ['TOKEN']
databaseid=os.environ['DATABASE_ID']

headers = {
    "Authorization": "Bearer"+token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

BOT_ID = client.api_call("auth.test")['user_id'] 

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    user = event.get('user')
    if BOT_ID != user_id:
        createPage(databaseid, headers, text) 
        client.chat_postMessage(channel = channel_id , text="snippet added to notion database.") 
    else:
        pass  


def createPage(databaseid, headers, text):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
         "parent": { "database_id": databaseid },
         "properties": {
		  "Name": {
			"title": [
				{
					"text": {
						"content": "Tuscan Kale"
					}
				}
			]
		},
        "log": {
			"rich_text": [
				{
					"text": {
						"content": text
					}
				 }
			  ] 
		   }
        }
    }

    data = json.dumps(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    if res.status_code==200:
        print('post successful')
    else:
        print('post unsuccessful')


if __name__ == "__main__" :
    app.run(debug=True)
    
    
