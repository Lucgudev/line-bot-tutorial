import requests, json
import re
import aiml
from Kernel import Kernel
from bs4 import BeautifulSoup
from collections import defaultdict
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
line_bot_api = LineBotApi('LY0u17AEiKkEyjdXniQDPyqWVgiE5eeS8BQgIM40CfHjC3PUJD+X68f1d33YOHjjFdzA2IIxFNb6/3KYxOh4dYXtEqX/wFOtrjbKOjteLnViC+66hfz/tHB8k3teAV6COCzXzJo4yGrpm1zNTGXiWgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e8dd62d53e807b4d4a91519e3667d2ae')



command = {
    "movie": "ok",
    "ngobrol":"ok",
    "berita":"ok"
}


kernel = aiml.Kernel()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def ngobrol():
    content = "Coklat si anjing coklat"
    return content

def movie():
    targetURL = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(targetURL, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 20:
            return content
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += title + "\n" + link + "\n"
    return content


def default_factory():
    return 'not command'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # cmd = defaultdict(default_factory, command)
    reply_command = ''' Woy ngapain coba-coba gue. Nih aturannya
     Welcome to crutcrutbot
    '''
    content = reply_command
    if event.message.text == "movie":
        content = movie()
    if event.message.text == "ngobrol":
        content = ngobrol()
    if event.message.text == "berita":
        content = beritaTerbaru()
    else:
        content = kernel.respond(event.message.text)
    # print("event.reply_token:",event.reply_token)
    # print("event.message.text:", event.message.text)
    print (content)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=content))


if __name__ == '__main__':
    app.run()
