import requests
import json
import re


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/63.0.3239.132 Safari/537.36"
headers = {
    'user-agent': user_agent,
}
search_base_url = 'https://bt.sou177.com/index.php?r=files/index&kw='

name_pattern = re.compile(r'\starget = "_blank">(.*)</a>')  # name
date_pattern = re.compile(
    r'<span class="label label-success">(\d{4}-\d{2}-\d{2})</span>') # date
filesize_pattern = re.compile(
    r'<span class="label label-warning">(\d+\.?\d+\s[GM]B)</span>')  # filesize
magnetic_pattern = re.compile(
    r'<li class="col-xs-12 list-group-item"><a href = "/index.php\?r=files/view&infohash=([0-9a-z]*)"\starget = "_blank">')  # magnetic

def get_magnetic_json_result_from_av_num(av_num):
    response = requests.get(search_base_url + av_num, headers=headers).text

    name = re.findall(name_pattern, response)
    date = re.findall(date_pattern, response)
    filesize = re.findall(filesize_pattern, response)
    magnetic = ['magnet:?xt=urn:btih:{}'.format(m)
        for m in re.findall(magnetic_pattern, response)]
    key_list = list(range(len(magnetic)))

    json_result = {key: {'name': n, 'date': d, 'filesize': f, 'magnetic': m} for key, n, d,
                   f, m in zip(key_list, name, date, filesize, magnetic)}
    return json_result

if __name__ == '__main__':
    json_result = get_magnetic_json_result_from_av_num('hello')
    print(json_result)





# pattern = r'<li class="col-xs-12 list-group-item"><a href = "/index.php\?r=files/view&infohash=([0-9a-z]*)" target = "_blank">(.*)</a><h4><span class="label label-success">(\d{4}-\d{2}-\d{2})</span> <span class="label label-warning">(\d+\.?\d+\s[GM]B)</span></h4></li>'
# result = re.findall(pattern, response)
# key_list = list(range(len(result)))
# print(result, len(result))

# patterns = [
#     re.compile(r'\starget = "_blank">(.*)</a>'), #name
#     re.compile(r'<span class="label label-success">(\d{4}-\d{2}-\d{2})</span>'), # date
#     re.compile(r'<span class="label label-warning">(\d+\.?\d+\s[GM]B)</span>'), # filesize
#     re.compile(r'<li class="col-xs-12 list-group-item"><a href = "/index.php\?r=files/view&infohash=([0-9a-z]*)"') # magnetic
# ]

# for n in result:
#     for i in n:
#         print(i)
# print(type(result))
# for n in result:
#     print(n, type(n))

# name = re.findall(name_pattern, response)
# date = re.findall(date_pattern, response)
# filesize = re.findall(filesize_pattern, response)
# magnetic = ['magnet:?xt=urn:btih:{}'.format(
#     m) for m in re.findall(magnetic_pattern, response)]


# key_list = list(range(len(magnetic)))
# json_result = {key: {'name': name, 'date': date, 'filesize': filesize, 'magnetic': magnetic}
#                for key, name, date, filesize, magnetic in zip(key_list, name, date, filesize, magnetic)}

# print(json_result)
