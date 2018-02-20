import requests
import json
import time
from urllib.parse import quote_plus
from sou177 import Magnetic_sou177


def get_url(url):
    response = requests.get(url).json()
    return response

def get_me():
    url = api_url + 'getMe'
    response = get_url(url)
    return response

def get_updates():
    # url = api_url + 'getUpdates?timeout=100'
    url = api_url + 'getUpdates'
    response = get_url(url)
    return response

def get_last_update_id_from_updates(updates):
    last_update_id = updates['result'][-1]['update_id']
    return last_update_id

def confirm_all_updates():
    updates = get_updates()
    if updates['result']:
        last_update_id = get_last_update_id_from_updates(updates)
        url = api_url + 'getUpdates?offset={}'.format(last_update_id+1)
        response = get_url(url)
        return response
    else:
        return None


def get_chat_id_from_message(message):
    chat_id = message['from']['id']
    return chat_id


def get_first_name_from_message(message):
    first_name = message['from']['first_name']
    return first_name


def get_text_from_message(message):
    text = message['text']
    return text


def get_last_chat_id_and_text():
    updates = get_updates()
    # 存在未读消息时，获取最近一条消息
    if 'result' in updates and updates['result']:
        message = updates['result'][-1]['message']
        chat_id = get_chat_id_from_message(message)
        text = get_text_from_message(message)
        return chat_id, text
    # 消息列表为空，返回 None
    else:
        return None, None


def send_message(chat_id, text):
    text = quote_plus(text)
    url = api_url + 'sendMessage?chat_id={}&text={}'.format(chat_id, text)
    response = get_url(url)
    return response


def send_message_to_last_chat_id(text):
    chat_id, _ = get_last_chat_id_and_text()
    response = send_message(chat_id, text)
    return response

if __name__ == '__main__':
    with open(r'.\token', 'r') as f:
        token = f.read()
    # print(token)
    api_url = 'https://api.telegram.org/bot{}/'.format(token)
    no_message_flag = {'ok': True, 'result': []}

    magnetic_sou177 = Magnetic_sou177()
    search_result = magnetic_sou177.get_search_result('MIDE-401')
    result = magnetic_sou177.gather_json_reslut_from_search_result(search_result)
    text = json.dumps(result[0])
    # print(type(res))
    example = 'www.fuli123.gq发布，福利资源，日日更新 | EYAN-038 MIAD-835 MEYD-071 MDV-012 QN-006 MUKD-354'
    print(type(text))
    print(type(example))
    print(example.encode('utf-8'), type(example.encode('utf-8')))
    print(text.encode('utf-8'), type(text.encode('utf-8')))
    # print(text.encode('utf-16'))
    # send_message(408371980, example)
    # send_message(408371980, text)
