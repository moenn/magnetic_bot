import requests
import json
import time
from urllib.parse import quote_plus
from sou177 import get_magnetic_json_result_from_av_num

class Bot(object):
    """docstring for Bot"""
    def __init__(self, arg):
        self.arg = arg
        

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

def preprocess_text_from_user(text):
    if text.startswith('/'):
        text = text.replace('/', '')
    if text.endswith('@magnetic_bot'):
        text = text.replace('@magnetic_bot', '')  
    return text

def gather_message_to_send_from_text(text):
    try:

        json_result = get_magnetic_json_result_from_av_num(text)
        message_to_send = []
        message_to_send.append('描述： {}\n日期: {}\n文件大小： {}'.format(
            json_result[0]['name'], json_result[0]['date'], json_result[0]['filesize']))
        message_to_send.append(json_result[0]['magnetic'])

        return message_to_send

    except:
        return None

def gather_data_from_updates(updates):
    data = {}
    data['chat_id'],data['text'] = get_last_chat_id_and_text(updates)
    data['first_name'] = get_first_name_from_updates(updates)
    data['chat_type'] = judge_last_chat_type(updates)
    if data['chat_type'] == 'group':
        data['group_id'] = updates['result'][-1]['message']['chat']['id']
    else:
        data['group_id'] = None
    
    print('{} {} {} {} {}'.format(data['chat_id'], data['text'], data['first_name'], data['chat_type'], data['group_id']))
    return data
    

def handle_start_message(data):
    # 群组聊天
    if data['chat_type'] == 'group':
        send_message(data['group_id'], start_message_group)
    elif data['chat_type'] == 'private':
        send_message(data['chat_id'], start_message_private)
    else:
        pass    

def handle_avnum_message(data):
    message_to_send = gather_message_to_send_from_text(data['text'])
    if data['chat_type'] == 'group':
        if message_to_send != None:
            for message in message_to_send:
                send_message(data['group_id'], message)
        else:
            send_message(data['group_id'], '@{} 未找到 {} 对应的磁力链接'.format(data['first_name'], data['text']))
    elif data['chat_type'] == 'private':
        if message_to_send != None:
            for message in message_to_send:
                send_message(data['chat_id'], message)
        else:
            send_message(data['chat_id'], '未找到 {} 对应的磁力链接'.format(data['text']))
    else:
        pass

def main():
    print('Bot starts.')
    # 清除所有历史消息
    confirm_all_updates(get_updates())
    while True:
        updates = get_updates()
        if updates['ok'] == True and updates['result']:
            confirm_all_updates(updates)
            data = gather_data_from_updates(updates)
            data['text'] = preprocess_text_from_user(data['text'])
            if data['text'] == 'start':
                handle_start_message(data)
            else:
                handle_avnum_message(data)
            # 接收到其他信息都使用其搜索磁力链接

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

    main()
