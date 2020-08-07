import logging
import os
import time

import schedule
from slack import WebClient
from slack.errors import SlackApiError
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)


def sendMessage(slack_client, msg):
    # make the POST request through the python slack client

    # check if the request was a success
    try:
        slack_client.chat_postMessage(
            channel='#bots',
            text=msg
        )  # .get()
    except SlackApiError as e:
        logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
        logging.error(e.response)


if __name__ == "__main__":
    load_dotenv()
    slack_token = os.environ['SLACK_BOT_TOKEN']

    slack_client = WebClient(token=slack_token)
    logging.debug("authorized slack client")

    # # For testing
    msg = "Hello world(manual)!"

    sendMessage(slack_client, "Hello world(manual)!")
    #schedule.every(60).seconds.do(lambda: sendMessage(slack_client, "Hello world(timer)!"))
    # schedule.every().monday.at("13:15").do(lambda: sendMessage(slack_client, msg))
    logging.info("entering loop")

    while True:
        schedule.run_pending()
        time.sleep(5)  # sleep for 5 seconds between checks on the scheduler
