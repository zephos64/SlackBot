# basic starter code for a class that can be expanded to handle callbacks, attachents (buttons, etc) and more!
import json
import os
import requests

class ImageLookup:

    def __init__(self, message):
        self.msg = message
        self.imgUrl = self.findImage(message)

    def getText(self):
        return self.msg

    def findImage(self, message):
        url = "https://www.googleapis.com/customsearch/v1?"
        url += "key=" + os.environ['GOOGLE_API_KEY']
        url += "&cx=" + os.environ['GOOGLE_ENGINE_ID']
        url += "&q=" + message
        url += "&searchType=image"

        r = requests.get(url=url)
        itemsList = json.loads(r.text)['items']
        return itemsList[0]['link']
        #return "https://vignette.wikia.nocookie.net/mrfz/images/e/e0/Mostima_icon.png/revision/latest/scale-to-width-down/125?cb=20200201060352"

    def getBlock(self):
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Found this for search: " + self.msg
                }
            }
        ]


    def getAttachment(self):
        return [
            {
                "blocks": [
                    {
                        "type": "image",
                        "image_url": self.imgUrl,
                        "alt_text": self.msg
                    }
                ]
            }
        ]
