import requests
import json
import re


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/63.0.3239.132 Safari/537.36"
headers = {
    'user-agent': user_agent,
    'Origin':'https://www.torrentkitty.tv'
}

search_base_url = 'https://www.torrentkitty.tv/search/'
name_pattern = re.compile(r'<td class="name">(.+)</td><td class="size">')
date_pattern = re.compile(r'<td class="date">(\d{4}-\d{2}-\d{2})</td>')
filesize_pattern = re.compile(r'<td class="size">(\d+\.+\d+\s[mk]b)</td>')
magnetic_pattern = re.compile(r'Detail</a><a href="(.*)" title=')

def get_magnetic_json_result_from_av_num_torrent_kitty(av_num):
    res = requests.get(search_base_url+av_num, headers=headers)
    res.encoding = 'utf-8'
    # print(res.encoding)
    content = res.text
    name = re.findall(name_pattern, content)
    # for n in name:
    #     print(n)
    # print(len(name))
    date = re.findall(date_pattern, content)
    # print(date, len(date))
    filesize = re.findall(filesize_pattern, content)
    # print(filesize, len(filesize))
    magnetic = re.findall(magnetic_pattern, content)
    # print(magnetic, len(magnetic))
    # for n in magnetic:
    #     print(n)

    key_list = list(range(len(magnetic)))

    json_result = {key: {'name': n, 'date': d, 'filesize': f, 'magnetic': m} for key, n, d,
                   f, m in zip(key_list, name, date, filesize, magnetic)}
    return json_result


if __name__ == '__main__':
    json_result = get_json_result_from_av_num_torrent_kitty('mide-332')
    print(json_result)