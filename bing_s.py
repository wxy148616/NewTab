# coding:utf-8
import json
import requests
from lxml import etree
import xml.etree.ElementTree as ET
from flask import Flask

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    url = 'https://cn.bing.com/dict/?mkt=zh-cn'
    response = requests.request("GET", url=url)
    response_html = etree.HTML(response.content)
    bing_body_list = response_html.xpath(
        "//div[@class='client_daily_word_content']/div[@class='client_daily_words_bar']//text()")
    # 初始化数据
    word, chinese, phonetic_symbol_e, phonetic_symbol_u = u'hello', u'你好', u"英 [hə'ləʊ]", u"美 [heˈləʊ]"

    if len(bing_body_list):
        word = bing_body_list.pop(0)
        chinese = bing_body_list.pop(-1)
        for phonetic_symbol in bing_body_list:
            if u"美[" in word:
                phonetic_symbol_u = phonetic_symbol
            elif u"英[" in word:
                phonetic_symbol_e = phonetic_symbol
    data = {
        "word": word,
        "chinese": chinese,
        "phonetic_symbol_e": phonetic_symbol_e,
        "phonetic_symbol_u": phonetic_symbol_u,
        }
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)
