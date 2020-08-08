import json
import logging

from slack import WebClient
from slack.errors import SlackApiError

import ChannelsSingleton

logging.basicConfig(level=logging.DEBUG)
channels = ChannelsSingleton.ChannelSingleton()
bot_channel = 'bots'  # encoded: C0185NC5SES


def getConversationsList(slack_client: WebClient):
    try:
        logging.debug("Getting list of all channels")
        response = slack_client.conversations_list(
        )
        assert response["channels"]

        channels.createMap(response["channels"])

        return response
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)


def sendMessage(slack_client: WebClient, msg):
    try:
        logging.debug("Sending message: {}".format(msg))
        response = slack_client.chat_postMessage(
            channel=channels.getChannelId(bot_channel),
            text=msg
        )
        assert response["message"]

        return response
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)


def updateMessage(slack_client: WebClient, new_msg, timestamp):
    try:
        logging.debug("Updating message: {}".format(new_msg))

        response = slack_client.chat_update(
            channel=channels.getChannelId(bot_channel),  # this is the encoded channel id, not the name
            ts=timestamp,
            text=new_msg
        )
        assert response["message"]

        return response
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)


def sendImg(slack_client: WebClient, filepath):
    try:
        response = slack_client.files_upload(
            channels=channels.getChannelId(bot_channel),  # note it's channel's'
            file=filepath
        )
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)

def jsonPPrint(json_data):
    json_formatted_str = json.dumps(json_data, indent=2)
    logging.debug(json_formatted_str)