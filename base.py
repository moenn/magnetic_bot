import requests
import json
import time
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/63.0.3239.132 Safari/537.36"
search_base_url = 'https://bt.sou177.com/index.php?r=files/index&kw='
home_url = 'https://bt.sou177.com'
headers = {
    'user-agent':user_agent,

}

def get_search_result(av_num):

    url = search_base_url + av_num
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    li = soup.find('li', 'col-xs-12 list-group-item')
    return li

def gather_magnetic(li):
    # /index.php?r=files/view&infohash=bf93b0afeaf0b879399c1f2f2d392baa8658f5cd
    magnetic = 'magnet:?xt=urn:btih:' + li.a['href'][33:]

    return magnetic

def get_magnetic(av_num):
    try:

        li = get_search_result(av_num)
        magnetic = gather_magnetic(li)
    
        return magnetic
    except:
        return None

def send_magnetic(chat_id, magnetic):
    content = send_message(chat_id, magnetic)
    return content


def get_url(url):
    response = requests.get(url)
    content_str = response.content.decode('utf-8')
    content_json = json.loads(content_str)
    return content_json


def get_me():
    url = api_url + 'getMe'
    content = get_url(url)
    return content


def get_updates():
    url = api_url + 'getUpdates?timeout=100'
    content = get_url(url)
    return content


def confirm_all_updates():
    updates = get_updates()
    if updates['result']:
        last_update_id = get_last_update_id_from_updates(updates)
        url = api_url + 'getUpdates?offset={}'.format(last_update_id+1)
        content = get_url(url)
        return content
    else:
        return None


def get_last_update_id_from_updates(updates):
    last_update_id = updates['result'][-1]['update_id']
    return last_update_id


def get_chat_id_from_message(message):
    chat_id = message['from']['id']
    return chat_id


def get_first_name_from_message(message):
    first_name = message['from']['first_name']
    return first_name


def get_text_from_message(message):
    text = message['text']
    return text


def get_last_chat_id_and_text(updates):
    # 存在未读消息时，获取最近一条消息
    if updates['result']:
        message = updates['result'][-1]['message']
        chat_id = get_chat_id_from_message(message)
        text = get_text_from_message(message)
        return chat_id, text
    else:
        return None, None


def send_message(chat_id, text):
    text = quote_plus(text)
    url = api_url + 'sendMessage?chat_id={}&text={}'.format(chat_id, text)
    content = get_url(url)
    return content


def send_message_to_last_chat_id(text):
    chat_id, _ = get_last_chat_id_and_text(get_updates())
    content = send_message(chat_id, text)
    return content


def main():
    print('bot run')
    while True:
        updates = get_updates()
        chat_id, text = get_last_chat_id_and_text(updates)
        if chat_id and text:
            if text == '/start':
                start_message = '你好，磁力链接娘在此！\n 把番号发给我，我回复给你磁力链接哦~'
                send_message(chat_id, start_message)
            else:
                magnetic = get_magnetic(text)
                if magnetic:
                    send_magnetic(chat_id, magnetic)
                else:
                    wrong_message = '对不起，{}的磁力链接未找到'.format(text)
                    send_magnetic(chat_id, wrong_message)
            confirm_all_updates()
        else:
            pass
        time.sleep(1)


if __name__ == '__main__':
    with open('token', 'r') as f:
        token = f.read()
    api_url = 'https://api.telegram.org/bot{}/'.format(token)
    main()
