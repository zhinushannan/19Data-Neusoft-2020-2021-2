# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherspiderItem(scrapy.Item):
    # 城市名称
    city = scrapy.Field()
    # 历史天气
    weather_history = scrapy.Field()
    # 天气统计
    weather_stat = scrapy.Field()
    # 历史风向统计
    wind_dir_stat = scrapy.Field()
    # 历史风力统计
    wind_power_stat = scrapy.Field()
    pass
