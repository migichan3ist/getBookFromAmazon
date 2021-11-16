import requests
import json
from bs4 import BeautifulSoup
import datetime
import time

# Slackに送る機能
WEB_HOOK_URL = ""

#今日の日付を取得
DATE_TODAY = datetime.date.today()
WHAT_DAY = DATE_TODAY.strftime('%A')

#URL情報

'''
###曜日の定義については以下の通りである。###
週４で働く。ホワイト企業のようだ

'Sunday': '',
'Monday': '売れ筋ランキング',
'Tuesday': 'ほしいものリストランキング',
'Wednesday': '売れ筋ランキング',
'Thursday': '',
'Friday': 'ほしいものリストランキング',
'Saturday': '',

'''

URL_INFORMATION = {
    'Sunday': '',
    'Monday': 'https://www.amazon.co.jp/gp/bestsellers/books/466282/ref=zg_bs_pg_1?ie=UTF8&pg=1',
    'Tuesday': 'https://www.amazon.co.jp/gp/most-wished-for/books/466282/ref=zg_mw_pg_1?ie=UTF8&pg=1',
    'Wednesday': 'https://www.amazon.co.jp/gp/bestsellers/books/466282/ref=zg_bs_pg_1?ie=UTF8&pg=1',
    'Thursday': '',
    'Friday': 'https://www.amazon.co.jp/gp/most-wished-for/books/466282/ref=zg_mw_pg_1?ie=UTF8&pg=1',
    'Saturday': '',
}

url_code = URL_INFORMATION[WHAT_DAY]

if url_code == '':
    exit()

html_doc = requests.get(url_code).text

#print(html_doc)
soup = BeautifulSoup(html_doc, 'html.parser')  # BeautifulSoupの初期化

topics = soup.find_all(
    "li", class_="zg-item-immersion")

#print(topics)
send_topic = soup.find(
    "title").text

requests.post(WEB_HOOK_URL, data=json.dumps({
    "type": "mrkdwn",
    "text": "TODAY TOPIC : " + send_topic
}))

requests.post(WEB_HOOK_URL, data=json.dumps({
    "type": "divider",
    "text": ""
}))

for rank, topic in enumerate(topics[:30]):
    time.sleep(1)
    # print(topic)
    # タイトル取得
    title_div = topic.select('.p13n-sc-truncate')
    #print(title_div)
    title = title_div[0].text.strip()
    print(title)
    # URL取得
    URL_div = topic.select(".a-link-normal")
    URL = "https://www.amazon.co.jp" + URL_div[0].get("href")
    # print(URL)
    # レビュー
    review_big = topic.find(
        "div", class_="a-icon-row a-spacing-none")
    
    if review_big != None:
        review_div = review_big.find(
            "span", class_="a-icon-alt")
        review = review_div.text
        # print(review)
    else:
        review = ""
    # コメント
    pre_comment = topic.find(
        "a", class_="a-size-small a-link-normal")
    
    if pre_comment != None:
        comment = pre_comment.text
    else:
        comment = ""

    # 価格
    pre_price = topic.find(
        "span", class_="p13n-sc-price")
    
    if pre_price != None:
        price = pre_price.text
    else:
        price = ""


    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "mrkdwn",
        "text": str(rank + 1) + "位：" + "<" + URL + "|" + title + ">"
    }))

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "mrkdwn",
        "text": "レビュー : " + review
    }))

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "mrkdwn",
        "text": "コメント数 : " + comment
    }))

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "mrkdwn",
        "text": "値段 : " + price + "円"
    }))

