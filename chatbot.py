# -*- coding: UTF-8 -*-

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

channelSecret = "LINE-CHANNEL-SECRET"
channelAccessToken = "LINE-CHANNEL-ACCESS-TOKEN"

linebotApi = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)

@app.route("/.well-known/pki-validation/<filename>")
def sslForFree(filename):
    with open("sslforfree.txt", "r") as fin:
        return fin.read()

# webhook callback endpoint
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message = TextMessage)
def handleMmessage(event):
    linebotApi.reply_message(event.reply_token, TextSendMessage(text = event.message.text))

if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 80)
    app.run(host = "0.0.0.0", port = 443, ssl_context = ("certificate.crt", "private.key"))

