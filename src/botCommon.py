import json
import logging

from slack import WebClient
from slack.errors import SlackApiError

logging.basicConfig(level=logging.DEBUG)
bot_channel = '#bots'
bot_channel_encoded = 'C0185NC5SES'

def sendMessage(slack_client: WebClient, msg):
    try:
        logging.debug("Sending message: {}".format(msg))
        response = slack_client.chat_postMessage(
            channel=bot_channel,
            text=msg
        )
        assert response["message"]

        return response
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)

def updateMessage(slack_client: WebClient, newMsg, timestamp, channelId):
    try:
        logging.debug("Updating message: {}".format(newMsg))

        response = slack_client.chat_update(
            channel=channelId, #this is the encoded channel id, not the name
            ts=timestamp,
            text=newMsg
        )
        assert response["message"]

        return response
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)

def sendImg(slack_client: WebClient, filepath):
    try:
        response = slack_client.files_upload(
            channels=bot_channel, # note it's channel's'
            file=filepath
        )
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)

def jsonPPrint(json_data):
    json_formatted_str = json.dumps(json_data, indent=2)
    logging.debug(json_formatted_str)