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

def main():
    print('Bot starts.')
    confirm_all_updates()
    while True:
        updates = get_updates()
        if updates == no_message_flag:
            pass
        else:
            chat_id, text = get_last_chat_id_and_text()
            print(chat_id, text)
            if chat_id and text:
                confirm_all_updates()
                if text == '/start' :
                    send_message(chat_id, start_message)
                else:
                    try:
                        magnetic_sou177 = Magnetic_sou177()
                        search_result = magnetic_sou177.get_search_result(text)
                        result = magnetic_sou177.gather_json_reslut_from_search_result(search_result)
                        message_to_send = []
                        message_to_send.append('描述： {}\n日期: {}\n文件大小： {}'.format(result[0]['name'], result[0]['date'], result[0]['filesize']))
                        message_to_send.append(result[0]['href'])

                        for m in message_to_send:
                            send_message(chat_id, m)
                    except:
                        send_message(chat_id, '未找到{}对应的磁力链接'.format(text))
            else:
                pass
        time.sleep(0.5)


if __name__ == '__main__':
    with open(r'token', 'r') as f:
        token = f.read()
    # print(token)
    api_url = 'https://api.telegram.org/bot{}/'.format(token)
    no_message_flag = {'ok': True, 'result': []}
    start_message = '你好，磁力链接娘！💕\n发送番号，得到对应的磁力链接哦~(例子：RBD-865)'
    # result = get_me()
    # confirm_all_updates()
    # result = get_updates()
    # print(result)
    
    main()

