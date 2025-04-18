from flask import Flask, request, abort
import os
import requests

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

@app.route("/", methods=["GET"])
def health_check():
    return "Webhook is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json()
    events = payload.get("events", [])

    for event in events:
        reply_token = event["replyToken"]
        user_msg = event["message"]["text"]

        reply(user_msg, reply_token)

    return "OK", 200

def reply(msg, reply_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": f"你說了：{msg}"
            }
        ]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=data)

if __name__ == "__main__":
    app.run()
