'''
批量地搜索 av 番号对应的磁力链接。
访问 "https://bt.sou177.com/index.php?r=files/index&kw= + av_num" 以获取搜索结果。
2018/1/16
'''
import requests
from bs4 import BeautifulSoup
import json
import re


class Magnetic_sou177(object):
    """docstring for Mgnetic_178"""
    def __init__(self):
        self.session = requests.Session()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/63.0.3239.132 Safari/537.36"     
        self.headers = {
            'user-agent':self.user_agent,
        }
        self.home_url = 'https://bt.sou177.com'
        self.search_base_url = 'https://bt.sou177.com/index.php?r=files/index&kw='

        self.session.headers.update(self.headers)

    def get_search_result(self, av_num):
        url = self.search_base_url + av_num
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        search_result = soup.find_all('li', 'col-xs-12 list-group-item')
        return search_result

    # def get_magnetic(self, li):
    #     magnetic =  + li.a['href'][33:]
    #     return magnetic

    def gather_json_reslut_from_search_result(self, search_result):
        
        href = []
        name = []
        date = []
        filesize = []



        for li in search_result:
            h = 'magnet:?xt=urn:btih:{}'.format(li.a['href'][33:]) # href
            href.append(h)
            n = li.get_text()


            d = re.findall(r'\d{4}-\d{2}-\d{2}', n) # date
            if d:
                date.append(d[0])
            else:
                date.append(None)

            f = re.findall(r'\d+\.?\d+\s[GM]B', n) # filesize
            if f:
                filesize.append(f[0])
            else:
                date.append(None)

            n = re.sub(r'\d{4}-\d{2}-\d{2}\s\d+\.?\d+\s[GM]B', '', n) # delete (date, filesize) in the name

            name.append(n)
            
            

        
        key_list = list(range(len(href)))
        json_result = {key:{'href':href,'name':name,'date':date,'filesize':filesize} for key,href,name,date,filesize in zip(key_list, href,name,date,filesize)}
        return json_result
        

if __name__ == '__main__':
    # pass
    magnetic_178 = Magnetic_sou177()
    search_result = magnetic_178.get_search_result('DVDES-644')
    result = magnetic_178.gather_json_reslut_from_search_result(search_result)
    print(result)



    # json_result = magnetic_178.gather_json_reslut_from_search_result(search_result)
    # print(json_result)
    # date_filesize_list = [] 
        #     date = child.get_text()
        #     file_size = child.get_text()
        # print(n.h4.children)
        # date_filesize_list.append(n.h4.get_text())
        # print(n.h4.get_text(), type(n.h4.get_text()))
        # print(n, type(n))
        # print(n.h4.span.get_text(), type(n.h4.span.get_text()))
#<li class="col-xs-12 list-group-item"><a href="/index.php?r=files/view&amp;infohash=bf93b0afeaf0b879399c1f2f2d392baa8658f5cd"
    # with open(r'./test.txt', 'w') as f:
    #     data = '\n'.join(date_filesize_list)
    #     f.write(data)
# target="_blank">henhei.gq发布，福利资源，日日更新 | IPZ-460 MUM-129 JUFD-407 JUFD-401 CND-114 MIDE-155 </a>
#<h4><span class="label label-success">2016-12-19</span> <span class="label label-warning">708.26 MB</span></h4></li> <class 'bs4.element.Tag'>


# /index.php?r=files/view&infohash=bf93b0afeaf0b879399c1f2f2d392baa8658f5cd
# 



        




