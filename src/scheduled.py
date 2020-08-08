import logging
import os
import time

import schedule
from dotenv import load_dotenv
from slack import WebClient

import BotCommon

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    load_dotenv()
    slack_token = os.environ['SLACK_BOT_TOKEN']

    slack_client = WebClient(token=slack_token)
    logging.debug("authorized slack client")

    # Sending text
    schedule.every(5).seconds.do(lambda: BotCommon.sendMessage(slack_client, "5s timer"))
    # schedule.every().monday.at("13:15").do(lambda: sendMessage(slack_client, msg))

    logging.info("entering loop")
    while True:
        schedule.run_pending()
        time.sleep(5)  # sleep for 5 seconds between checks on the scheduler
