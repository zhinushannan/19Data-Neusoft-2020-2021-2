import re

from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
import json


class Covid:
    def __init__(self):
        html = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia').content.decode()
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find(attrs={'id': 'getListByCountryTypeService2true'})
        json_data_str = re.findall(r'\[.+]', str(data))[0]
        self.json_data = json.loads(json_data_str)

    def parse_data(self, country):
        print('正在获取数据')
        country_data = {}
        for i in self.json_data:
            if i['provinceName'] == country:
                country_data = {
                    '国家': i['provinceName'],
                    '累计确诊人数': i['confirmedCount'],
                    '现有确诊人数': i['currentConfirmedCount'],
                    '累计治愈人数': i['curedCount'],
                    '累计死亡人数': i['deadCount'],
                    '新增确诊人数': i['incrVo']['confirmedIncr'],
                    '新增治愈人数': i['incrVo']['curedIncr'],
                    '新增死亡人数': i['incrVo']['deadIncr']
                }
                break
        return country_data

    def get_history(self, country):
        url = ''
        for i in self.json_data:
            if i['provinceName'] == country:
                url = i['statisticsData']
        return requests.get(url).content.decode()

    def parse_data_history(self, country):
        print('正在获取数据')
        src_data = ''
        for i in self.json_data:
            if i['provinceName'] == country:
                src_data = requests.get(i['statisticsData']).content.decode()
        json_data = json.loads(src_data)['data']
        data_list = {}
        for i in json_data:
            data = {
                '日期': str(i['dateId']),
                '累计确诊人数': i['confirmedCount'],
                '现有确诊人数': i['currentConfirmedCount'],
                '累计治愈人数': i['curedCount'],
                '累计死亡人数': i['deadCount'],
                '新增确诊人数': i['confirmedIncr'],
                '新增治愈人数': i['curedIncr'],
                '新增死亡人数': i['deadIncr']
            }
            data_list[i['dateId']] = data
        return data_list

    def save(self, data, fileName):
        with open(f'./json_data/{fileName}', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def draw(self, data, title, saveNeeded):
        print('正在绘图')
        time = list(data.keys())
        x_data = []
        for i in range(0, len(time), 20):
            x_data.append(str(time[i]))
        y1 = []  # 累计确诊人数
        y2 = []  # 现有确诊人数
        y3 = []  # 累计治愈人数
        y4 = []  # 累计死亡人数
        for i in x_data:
            y1.append(data[int(i)]['累计确诊人数'])
            y2.append(data[int(i)]['现有确诊人数'])
            y3.append(data[int(i)]['累计治愈人数'])
            y4.append(data[int(i)]['累计死亡人数'])
        plt.figure(figsize=(20, 8), dpi=80)
        plt.plot(x_data, y1, label='累计确诊人数')
        plt.plot(x_data, y2, label='现有确诊人数')
        plt.plot(x_data, y3, label='累计治愈人数')
        plt.plot(x_data, y4, label='累计死亡人数')
        plt.xlabel('日期')
        plt.ylabel('数量')
        plt.title(title)
        plt.legend()
        plt.show()
        if saveNeeded:
            print('正在保存图片')
            plt.savefig(f'./img/{title}.jpg')

    def run(self, country='中国', historyNeeded=False, dataSaveNeeded=False, plotNeeded=False, plotSaveNeed=False):
        fileName = country + '的'
        if historyNeeded:
            result = self.parse_data_history(country=country)
            fileName = fileName + '所有数据.json'
            if plotNeeded:
                title = f'{country}数据折线图'
                self.draw(data=result, title=title, saveNeeded=plotSaveNeed)
        else:
            result = self.parse_data(country=country)
            fileName = fileName + '当日数据.json'
        if dataSaveNeeded:
            result_data = []
            keys = list(result.keys())
            for i in keys:
                print(result[i])
                result_data.append(result[i])
            self.save(result_data, fileName)
        print('数据如下', '\n', result)


if __name__ == '__main__':
    country = input('请输入需要查询的国家:')
    historyNeeded = input('是否需要查询历史所有数据？(y/n):')
    historyNeeded = historyNeeded == 'y' or historyNeeded == 'Y'

    plotNeeded = False
    plotSaveNeed = False
    if historyNeeded:
        plotNeeded = input('是否需要绘图？(y/n):')
        plotNeeded = plotNeeded == 'y' or plotNeeded == 'Y'
        if plotNeeded:
            plotSaveNeed = input('所绘的图是否需要保存？(y/n):')
            plotSaveNeed = plotSaveNeed == 'y' or plotSaveNeed == 'Y'

    dataSaveNeeded = input('所获得的数据是否需要保存？(y/n):')
    dataSaveNeeded = dataSaveNeeded == 'y' or dataSaveNeeded == 'Y'

    Covid().run(country=country, historyNeeded=historyNeeded, dataSaveNeeded=dataSaveNeeded, plotNeeded=plotNeeded, plotSaveNeed=plotSaveNeed)
