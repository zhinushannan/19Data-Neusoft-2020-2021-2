import json
import random

import requests
from bs4 import BeautifulSoup


class Movie:
    def __init__(self, encoding='gbk'):
        # 电影类别
        self.category = {
            '动作片': 2,
            '剧情片': 0,
            '爱情片': 3,
            '喜剧片': 1,
            '科幻片': 4,
            '恐怖片': 8,
            '动画片': 5,
            '惊悚片': 7,
            '战争片': 14,
            '犯罪片': 15,
        }
        # url
        self.url = 'https://www.dy2018.com/{}/index{}.html'
        # 请求头
        self.headers = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        ]
        self.encoding = encoding

    def get_response(self, url):
        header = self.headers[0]
        return requests.get(url=url, headers=header).content.decode(encoding=self.encoding)

    def parse_data(self, html):
        soup = BeautifulSoup(html)
        movie_table_set = soup.find_all(attrs={'class': 'tbspan'})
        movie_url_list = []
        for i in range(0, len(movie_table_set)):
            print(f'------------开始获取该页第{i + 1}条电影数据')
            movie_url_list.append('https://www.dy2018.com' + movie_table_set[i].find_all('tr')[1].find_all('a')[1].get('href'))

        movie_list = []
        for i in movie_url_list[0:30]:
            movie_detail = self.get_response(i)
            movie = self.parse_movie(movie_detail)
            movie_list.append(movie)
        return movie_list

    def parse_movie(self, movie_detail):
        soup_temp = BeautifulSoup(movie_detail)
        soup_details_temp = soup_temp.find(attrs={'id': 'Zoom'})
        details_temp = str(soup_details_temp).split('<br/>')
        player_list_url = '官方未提供此链接'
        if soup_details_temp.find(attrs={'class': 'player_list'}) is not None:
            player_list_url = \
                str(soup_details_temp.find(attrs={'class': 'player_list'}).find('a').get('href')).split('=')[-1]
        bt_url = '官方未提供此链接'
        if soup_temp.find(attrs={'id': 'downlist'}) is not None:
            bt_url = str(soup_temp.find(attrs={'id': 'downlist'}).find('a').get('href'))

        if len(details_temp) != 1:
            movie = {
                '译名': details_temp[1][6:],
                '片名': details_temp[2][6:],
                '年代': details_temp[3][6:],
                '产地': details_temp[4][6:],
                '类别': details_temp[5][6:],
                '语言': details_temp[6][6:],
                '字幕': details_temp[7][6:],
                '上映日期': details_temp[8][6:],
                '豆瓣评分': details_temp[9][6:],
                'IMDb评分': details_temp[10][7:],
                '视频大小': details_temp[11][6:],
                '片长': details_temp[12][6:],
                '导演': details_temp[13][6:],
                '简介': details_temp[15][6:],
                '专属下载器下载链接': player_list_url,
                'bt下载链接': bt_url
            }
        else:
            details_temp = str(soup_details_temp).split('<p>')
            movie = {
                '译名': details_temp[2][6:-5],
                '片名': details_temp[3][6:-5],
                '年代': details_temp[4][6:-5],
                '产地': details_temp[5][6:-5],
                '类别': details_temp[6][6:-5],
                '语言': details_temp[7][6:-5],
                '字幕': details_temp[8][6:-5],
                '上映日期': details_temp[9][6:-5],
                '视频大小': details_temp[12][6:-5],
                '片长': details_temp[13][6:-5],
                '导演': details_temp[14][6:-5],
                '简介': details_temp[30][6:-5],
                '专属下载器下载链接': player_list_url,
                'bt下载链接': bt_url
            }
        return movie

    def write_to_file(self, movie_data):
        with open('./json/13-Movie.json', 'w', encoding='utf-8') as f:
            json.dump(obj=movie_data, fp=f, ensure_ascii=False, indent=4, separators=(',', ':'))

    def run(self, category='动作片', page=5):
        result = {}
        for i in range(1, page + 1):
            url = self.url.format(self.category[category], f'_{page}' if page != 1 else '')
            print(f'开始获取第{i}页电影数据')
            html = self.get_response(url)
            result[f'page{i}'] = self.parse_data(html)
        print('开始保存文件，程序即将运行结束')
        movie_data = {'Movie': result}
        self.write_to_file(movie_data)


if __name__ == '__main__':
    Movie().run()
