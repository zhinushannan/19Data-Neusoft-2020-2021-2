import scrapy

from weatherSpider.items import WeatherspiderItem
from weatherSpider.pipelines import WeatherspiderPipeline
import json


class TianqiSpider(scrapy.Spider):
    name = 'tianqi'
    allowed_domains = ['lishi.tianqi.com']
    start_urls = ['http://lishi.tianqi.com/']

    def parse(self, response):
        selectors = response.xpath('//tbody/tr')
        for selector in selectors:
            initial = selector.xpath('./th/a/text()')
            if len(initial) == 0:
                continue
            cities = selector.xpath('./td/ul/li')
            for c in cities:
                url = 'http://lishi.tianqi.com/' + c.xpath('./a/@href').get()
                print(f'url组装完成{url}')
                yield scrapy.Request(url=url, callback=self.parse_detail)
                # return
            # return

    def parse_detail(self, response):
        print(f'开始获取{response.request.url}...', end='')

        # 城市名称
        city = response.xpath('//div[@class="tian_one"]/div[@class="flex"]/h3/text()').get()

        # ------------------------
        # 历史天气
        # - 温度
        temperature = {
            # 平均高温
            'high_avg': response.xpath('//ul[@class="tian_two"]/li[1]/div[1]/div[1]/text()').get(),
            # 平均低温
            'low_avg': response.xpath('//ul[@class="tian_two"]/li[1]/div[2]/div[1]/text()').get(),
            # 极端高温
            'highest': response.xpath('//ul[@class="tian_two"]/li[2]/div[1]/text()').get(),
            # 极端低温
            'lowest': response.xpath('//ul[@class="tian_two"]/li[3]/div[1]/text()').get()
        }
        # - 空气质量
        atmosphere = {
            # 平均空气质量指数
            'avg': response.xpath('//ul[@class="tian_two"]/li[4]/div[1]/text()').get(),
            # 空气最好
            'best': response.xpath('//ul[@class="tian_two"]/li[5]/div[1]/text()').get(),
            # 空气最差
            'worst': response.xpath('//ul[@class="tian_two"]/li[6]/div[1]/text()').get(),
        }
        # - 天气详情
        details_response = response.xpath('//div[@class="tian_three"]/ul/li')
        details = []
        for i in details_response:
            detail = {
                # 日期
                'date': i.xpath('./div[1]/text()').get(),
                # 最高气温
                'highest': i.xpath('./div[2]/text()').get(),
                # 最低气温
                'lowest': i.xpath('./div[3]/text()').get(),
                # 天气
                'weather': i.xpath('./div[4]/text()').get(),
                # 风向
                'wind_dir': i.xpath('./div[5]/text()').get(),
            }
            details.append(detail)
        weather_history = {
            'temperature': temperature,
            'atmosphere': atmosphere,
            'details': details
        }

        # -------------------------
        # 天气统计
        weather_stat = response.xpath('/html/body/div[7]/div[1]/div[6]/div/div[2]/text()').get()

        # -----------------------
        # 历史风向统计
        wind_dir_stat = []
        dir_stat_response = response.xpath('/html/body/div[7]/div[1]/div[9]/div/div[2]/ul/li')
        for i in range(1, len(dir_stat_response) - 1):
            wind_dir_stat.append(dir_stat_response[i].xpath('./text()').get())

        # -----------------------
        # 历史风力统计
        wind_power_stat = []
        wind_power_response = response.xpath('/html/body/div[7]/div[1]/div[12]/div/div[2]/ul/li')
        for i in range(1, len(wind_power_response) - 1):
            wind_power_stat.append(wind_power_response[i].xpath('./text()').get())

        item = WeatherspiderItem()
        item['city'] = city
        item['weather_history'] = weather_history
        item['weather_stat'] = weather_stat
        item['wind_dir_stat'] = wind_dir_stat
        item['wind_power_stat'] = wind_power_stat

        print('结束')

        yield WeatherspiderPipeline.process_item(self, item, self)
