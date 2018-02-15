import requests
import json
import time
from urllib.parse import quote_plus





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
    while True:
        updates = get_updates()
        chat_id, text = get_last_chat_id_and_text(updates)
        if chat_id and text:
            print(chat_id, text)
            send_message_to_last_chat_id(text)
            confirm_all_updates()
        else:
            pass
        time.sleep(1)

if __name__ == '__main__':
    with open('token', 'r') as f:
        token = f.read()
    api_url = 'https://api.telegram.org/bot{}/'.format(token)
    main()

