# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os


class WeatherspiderPipeline:
    def process_item(self, item, spider):
        print('进入管道')
        filename = f'./jsondata/{item["city"]}.json'
        if not os.path.exists('./jsondata'):
            os.mkdir('./jsondata')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dict(item), f, ensure_ascii=False, indent=4)
            # f.write(str(item))
