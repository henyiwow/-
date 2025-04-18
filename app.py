from flask import Flask, request, abort
import os
import json
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# LINE Bot 設定
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Webhook 接收事件
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理收到的訊息
@handler.add(event='message')
def handle_message(event):
    text = event.message.text  # 取得用戶發送的訊息
    reply_token = event.reply_token
    line_bot_api.reply_message(reply_token, TextSendMessage(text='收到你的訊息: ' + text))

if __name__ == "__main__":
    app.run(debug=True)
