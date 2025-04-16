import os
import requests

LINE_API_URL = "https://api.line.me/v2/bot/message/push"

LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_TO = os.getenv("LINE_TO")

def send_line_message(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_TO,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    response = requests.post(LINE_API_URL, headers=headers, json=data)
    print("LINE API 回應:", response.status_code, response.text)
