import os
import logging
import time
from threading import Thread

from dotenv import load_dotenv
from flask import Flask, request, make_response

from slack.web.client import WebClient
from slack.errors import SlackApiError
from slack.signature import SignatureVerifier

from python.slashCommands.msgCmd import Slash
from python.slashCommands.msgLookupCmd import ImageLookup


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route("/slack/zecho", methods=["POST"])
def echoCmd():
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("invalid request", 403)
    info = request.form

    # # send user a response via DM
    # im_id = slack_client.im_open(user=info["user_id"])["channel"]["id"]
    # ownerMsg = slack_client.chat_postMessage(
    #   channel=im_id,
    #   text=commander.getMessage()
    # )

    try:
        # Echo some text back
        response = slack_client.chat_postMessage(
            channel='#{}'.format(info["channel_name"]),
            text="Echoing message - " + info['text']
        )

    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)
        return make_response("", e.response.status_code)

    return make_response("", response.status_code)


@app.route("/slack/zimglookup", methods=["POST"])
def dmImgLookupCmd():
    if not verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("invalid request", 403)
    info = request.form
    try:
        # Immediately acknowledge response, or we'll get an error
        response = slack_client.chat_postMessage(
            channel='#{}'.format(info["channel_name"]),
            text="Searching for " + info['text'] + "..."
        )

        # Spawn separate thread for searching, update prev response when found
        #  Unsure if this is a good practice, but it works
        thr = Thread(target=asyncImageLookup, args=[response['channel'], info['text'],
                                                    response['ts']])
        thr.start()

    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)
        return make_response("", e.response.status_code)

    return make_response("", response.status_code)

def asyncImageLookup(encoded_channel_id, text, ts):
    time.sleep(3)

    # Look up the image
    msgLookup = ImageLookup(text)
    response = slack_client.chat_update(
        channel=encoded_channel_id,
        ts=ts,
        blocks=msgLookup.getBlock(),
        attachments=msgLookup.getAttachment()
    )

# Start the Flask server
if __name__ == "__main__":
    load_dotenv()
    SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
    SLACK_SIGNATURE = os.environ['SLACK_SIGNATURE']
    slack_client = WebClient(SLACK_BOT_TOKEN)
    verifier = SignatureVerifier(SLACK_SIGNATURE)

    #BotCommon.getConversationsList(slack_client)
    #resp = BotCommon.sendMessage(slack_client, "Zephbot started up")

    app.run(port=80)
