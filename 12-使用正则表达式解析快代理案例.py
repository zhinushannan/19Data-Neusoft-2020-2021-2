import random
import requests
from bs4 import BeautifulSoup
import json

class Kuaiproxy:
    def __init__(self):
        self.url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.headers = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
        ]
        self.datas = []

    def get_response(self, url):
        header = self.headers[random.randint(0, len(self.headers) - 1)]
        return requests.get(url=url, headers=header).content.decode()

    def parse_data(self, data):
        html = BeautifulSoup(data, 'html.parser')
        datas = html.find_all('tr')
        result = []
        for i in range(1, len(datas)):
            ip = datas[i].find(attrs={'data-title': 'IP'}).getText()
            port = datas[i].find(attrs={'data-title': 'PORT'}).getText()
            anonymity = datas[i].find(attrs={'data-title': '匿名度'}).getText()
            type = datas[i].find(attrs={'data-title': '类型'}).getText()
            area = datas[i].find(attrs={'data-title': '位置'}).getText()
            speed = datas[i].find(attrs={'data-title': '响应速度'}).getText()
            verify_time = datas[i].find(attrs={'data-title': '最后验证时间'}).getText()
            proxy = {
                'ip': ip,
                'port': port,
                '匿名度': anonymity,
                '类型': type,
                '位置': area,
                '响应速度': speed,
                '最后验证时间': verify_time
            }
            result.append(proxy)
        return result

    def write_to_file(self):
        data = {'data': self.datas}
        print(data)
        # data_json = json.dumps(data)
        with open('./json/proxy.json', 'w', encoding='gbk') as f:
            json.dump(data, f, ensure_ascii=False)
        pass

    def run(self, page=5):
        result = []
        for i in range(0, page):
            url = self.url.format(i + 1)
            html = self.get_response(url)
            data = self.parse_data(html)
            result.extend(data)
        self.datas.extend(result)
        self.write_to_file()
        pass


if __name__ == '__main__':
    Kuaiproxy().run(page=5)
