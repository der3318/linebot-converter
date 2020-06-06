# -*- coding: UTF-8 -*-

import sys
import ssl
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import tensorflow as tf
from basic import Dictionary, Sentence
from reader import HistoryReader
from model import SequenceToSequenceModel

app = Flask(__name__)

channelSecret = "LINE-CHANNEL-SECRET"
channelAccessToken = "LINE-CHANNEL-ACCESS-TOKEN"

if len(sys.argv) > 2:
    channelSecret = sys.argv[1]
    channelAccessToken = sys.argv[2]

linebotApi = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)

historyReader = HistoryReader("./history.txt")
dictionary = historyReader.readAndProcess()

# webhook callback endpoint
@app.route("/webhook", methods = ["POST"])
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

    seqToSeqModel = SequenceToSequenceModel(dictionary.size)
    tensorflowGraph = tf.get_default_graph()
    seqToSeqModel.loadWeights()

    sentence = Sentence()
    sentence.addGram(Dictionary.BOS)
    for idx, token in enumerate(event.message.text):
        if idx >= seqToSeqModel.sentenceLength:
            break
        sentence.addGram(dictionary.convertTokenToGram(token))
    if sentence.length() < seqToSeqModel.sentenceLength:
        sentence.addGram(Dictionary.EOS)

    with tensorflowGraph.as_default():
        response = seqToSeqModel.predict(sentence, dictionary)
        linebotApi.reply_message(event.reply_token, TextSendMessage(text = str(response)))

if __name__ == "__main__":
    # cat certificate.crt > chain.pem
    # echo "" >> chain.pem
    # cat ca_bundle.crt >> chain.pem
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ctx.load_cert_chain("chain.pem", "private.key")
    app.run(host = "0.0.0.0", port = 443, ssl_context = ctx)

