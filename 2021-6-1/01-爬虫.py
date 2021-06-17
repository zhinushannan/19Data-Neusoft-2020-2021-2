import requests

from bs4 import BeautifulSoup
import json


class GreatMan:
    def __init__(self):
        self.url = 'http://www.12371.cn/special/sflrw/'

    def get_requests(self, url):
        return requests.get(url).content.decode()

    def parse_data(self, src_data):
        soup = BeautifulSoup(src_data)

        # attrs = {}   id、class
        soup = soup.find(attrs={'class': 'showMoreNChildren'})
        soup = soup.find_all('li')

        great_man_list = []
        for i in soup:
            great_man_url = i.find_all('a')[1].get('href')
            html = self.get_requests(great_man_url)
            html_soup = BeautifulSoup(html)
            detail_title = html_soup.find(attrs={'class': 'big_title'}).getText()

            detail_soup = html_soup.find(attrs={'class': 'word'})
            detail_img = 'http:' + detail_soup.find('img').get('src')
            detail_img_describe = detail_soup.find('img').get('alt')

            detail_contents = detail_soup.find_all(attrs={'data-spm-anchor-id': '0.0.0.i1'})
            detail_content = ''
            for j in detail_contents:
                detail_content += '\n' + j.getText()
            great_man = {
                'title': i.find_all('a')[1].getText(),
                'img': 'http:' + i.find('img').get('src'),
                'url': i.find_all('a')[1].get('href'),
                'detail': {
                    'title': detail_title,
                    'img': detail_img,
                    'img-describe': detail_img_describe,
                    'content': detail_content
                }
            }
            great_man_list.append(great_man)
        return great_man_list

    def write_to_file(self, data):
        data = {'result': data}
        with open('./json/风流人物.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def run(self):
        src_data = self.get_requests(self.url)
        data = self.parse_data(src_data)
        self.write_to_file(data)
        pass


if __name__ == '__main__':
    GreatMan().run()
