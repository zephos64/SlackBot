class CoinFlip:
    def getInitBlock(self):
        return [
                {
                    "type": "actions",
                    "block_id": "coinFlipGame",
                    "elements": [
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Heads or Tails?"
                            },
                            "action_id": "select_2",
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Heads"
                                    },
                                    "value": "coin.heads"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Tails"
                                    },
                                    "value": "coin.tails"
                                }
                            ]
                        }
                    ]
                }
            ]
