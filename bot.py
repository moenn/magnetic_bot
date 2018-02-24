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


def confirm_all_updates(updates):
    if updates['result']:
        last_update_id = get_last_update_id_from_updates(updates)
        url = api_url + 'getUpdates?offset={}'.format(last_update_id+1)
        response = get_url(url)
        return response
    else:
        return None


def get_first_name_from_updates(updates):
    first_name = updates['result'][-1]['message']['from']['first_name']
    return first_name


def get_chat_id_from_updates(updates):
    chat_id = updates['result'][-1]['message']['from']['id']
    return chat_id


def get_text_from_updates(updates):
    text = updates['result'][-1]['message']['text']
    return text


def get_last_chat_id_and_text(updates):
    # updates = get_updates()
    # 存在未读消息时，获取最近一条消息
    # if 'result' in updates and updates['result']:
    message = updates['result'][-1]['message']
    chat_id = get_chat_id_from_updates(updates)
    text = get_text_from_updates(updates)
    return chat_id, text
    # 消息列表为空，返回 None
    # else:
    #     return None, None


def send_message(chat_id, text):
    text = quote_plus(text)
    url = api_url + 'sendMessage?chat_id={}&text={}'.format(chat_id, text)
    response = get_url(url)
    return response



def judge_last_chat_type(updates):
    type_ = updates['result'][-1]['message']['chat']['type']
    return type_


def gather_message_to_send_from_text(text):
    if text.startswith('/'):
        text = text.replace('/', '')
    if text.endswith('@magnetic_bot'):
        text = text.replace('@magnetic_bot', '')
    try:
        magnetic_sou177 = Magnetic_sou177()
        search_result = magnetic_sou177.get_search_result(text)
        result = magnetic_sou177.gather_json_reslut_from_search_result(
            search_result)
        message_to_send = []
        message_to_send.append('描述： {}\n日期: {}\n文件大小： {}'.format(
            result[0]['name'], result[0]['date'], result[0]['filesize']))
        message_to_send.append(result[0]['href'])

        return message_to_send

    except:
        return None

def gather_data_from_updates(updates):
    chat_id, text = get_last_chat_id_and_text(updates)
    first_name = get_first_name_from_updates(updates)
    chat_type = judge_last_chat_type(updates)
    if chat_type == 'group':
        group_id = updates['result'][-1]['message']['chat']['id']
    else
        group_id = None
    return chat_id, text, first_name, chat_type, group_id

def main():
    print('Bot starts.')
    # 清除所有历史消息
    confirm_all_updates(get_updates())
    while True:
        updates = get_updates()
        if updates['ok'] == True and updates['result']:
            confirm_all_updates(updates)
            chat_id, first_name, text, chat_type, group_id = gather_data_from_updates(updates)
            print(chat_id, first_name, text, chat_type, group_id)
            # 接收到 /start
            if text == '/start':
                if not group_id:
                    send_message(chat_id, start_message_private)
            elif text == '/start@magnetic_bot':
                if group_id:
                    send_message(group_id, start_message_group)
            # 接收到其他信息都使用其搜索磁力链接
            else:
                message_to_send = gather_message_to_send_from_text(text)
                if chat_type == 'private':
                    if message_to_send:
                        for message in message_to_send:
                            send_message(chat_id, message)
                    else:
                        send_message(chat_id, '未找到 {} 对应的磁力链接'.format(text))
                elif chat_type == 'group':
                    if message_to_send:
                        for message in message_to_send:
                            send_message(group_id, message)
                    else:
                        send_message(group_id, '@{} 未找到 {} 对应的磁力链接'.format(first_name, text))
                else:
                    pass
        else:
            pass
        time.sleep(0.5)



if __name__ == '__main__':
    # 读取 token 等
    with open(r'config', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
    token = config['token']
    start_message_private = config['start_message_private']
    start_message_group = config['start_message_group']

    api_url = 'https://api.telegram.org/bot{}/'.format(token)
    # result = get_me()
    # confirm_all_updates()
    # result = get_updates()
    # print(result)

    main()
