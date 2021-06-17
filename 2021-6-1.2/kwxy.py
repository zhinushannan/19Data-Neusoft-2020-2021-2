import requests

from bs4 import BeautifulSoup

import json


class Kwxy:
    def __init__(self):
        self.url = 'http://kwxy.jsnu.edu.cn/10048/list{}.htm'

    def get_requests(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Host': 'kwxy.jsnu.edu.cn'
        }
        return requests.get(url=url, headers=headers).content.decode()

    def parse_data(self, src_data):
        soup = BeautifulSoup(src_data)
        soup = soup.find(attrs={'id': 'wp_news_w9'})

        news_list = []

        a_soup_list = soup.find_all('a')
        date_soup_list = soup.find_all(attrs={'class': 'column-news-date news-date-hide'})
        for i in range(1, len(a_soup_list), 2):
            detail_url = a_soup_list[i].get('href')
            if detail_url.startswith('http'):
                continue
            detail_url =  'http://kwxy.jsnu.edu.cn' + detail_url
            html = self.get_requests(detail_url)
            html_soup = BeautifulSoup(html).find(attrs={'class': 'article'})
            detail_title = html_soup.find(attrs={'class': 'arti-title'}).getText()
            detail_date = html_soup.find(attrs={'class': 'arti-update'}).getText()
            detail_view = html_soup.find(attrs={'class': 'WP_VisitCount'}).getText()

            detail_content_list = html_soup.find_all(attrs={'class': 'p_text_indent_2'})
            detail_content = ''
            for j in detail_content_list:
                if j.find('span') is not None:
                    detail_content += j.find('span').getText()
                    continue
                detail_content += j.getText()

            detail_imgs_list = html_soup.find_all('img')
            detail_imgs = []
            for j in detail_imgs_list:
                img = {
                    'img-url': 'http://kwxy.jsnu.edu.cn' + str(j.get('original-src')),
                    'img-describe': j.get('sudyfile-attr')
                }
                detail_imgs.append(img)

            news = {
                'title': a_soup_list[i].get('title'),
                'url': 'http://kwxy.jsnu.edu.cn' + a_soup_list[i].get('href'),
                'date': date_soup_list[i // 2].getText(),
                'detail': {
                    'title': detail_title,
                    'date': detail_date,
                    'view': detail_view,
                    'content': detail_content,
                    'imgs': detail_imgs
                }
            }

            news_list.append(news)
        return news_list

    def write_to_file(self, data, page):
        data = {'data': data}
        with open(f'./json/第{page + 1}页.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self, page=5):
        for i in range(0, page):
            url = self.url.format(i + 1)
            src_data = self.get_requests(url)
            result = self.parse_data(src_data)
            self.write_to_file(result, i)


if __name__ == '__main__':
    Kwxy().run()
