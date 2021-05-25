import requests
import json


# 请求首页的tag值的
# https://movie.douban.com/j/search_tags?type=tv&source=
# 请求电视数据的
# "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0"


class TVTag:
    @classmethod
    def get_tv_tags(cls):
        """
        获取所有的tag
        """
        # tag所在的请求地址
        url = "https://movie.douban.com/j/search_tags?type=tv&source="
        # 构造请求头
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        # 发送请求
        response = requests.get(url=url, headers=header)
        # tag数据
        tag_dict = json.loads(response.content.decode())
        # 处理数据
        # 创建临时的数据列表用来存储tag
        tag = []
        for t in tag_dict['tags']:
            tag.append(t)
        return tag


class DBTV:
    def __init__(self, tag, page_limit=50):
        """
        初始化方法
        """
        # 构造请求地址
        self.url = "https://movie.douban.com/j/search_subjects?type=tv&tag=" + tag + "&sort=recommend&page_limit=" + str(page_limit) + "&page_start=0"
        # 构造请求头
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        # 定义数据源用来存储处理好的电视数据
        self.datas = []
        # 定义数据文件的存储路径
        self.file_path = './data/'

    def get_resposne(self, url):
        """
        发送请求并获取响应
        """
        return requests.get(url=url, headers=self.header).content.decode()

    def parse_data(self, content):
        """
        解析数据（从响应中提取需要的数据）
        功能1： 提取电视剧姓名（完成）
        功能2： 提取电视剧评分（完成）
        功能3： 提取电视剧的缩略图（未完成）
        """
        # 1. 将json字符串转换成python的字典类型（方便提取数据）
        data = json.loads(content)
        # 2. 提取数据
        for t in data["subjects"]:
            # 定义字典用来保存提取的电视信息
            tv = {}
            # 获取电视剧名称
            tv['name'] = t['title']
            # 获取电视剧的评分
            tv['rate'] = t['rate']
            # 每处理一个电视剧就将结果拼接到数据源中
            self.datas.append(tv)

    def run(self):
        """
        爬虫启动程序
        """
        # 1. 发送请求
        content = self.get_resposne(self.url)
        # 2. 解析数据
        self.parse_data(content)
        # 验证数据是否存储完毕
        # 3. 存储数据
        # 3.1 数据持久化
        # 3.1.1 将数据存储到文件中（txt，json，csv）
        # 3.1.2 将数据存储到数据库中（非关系型数据库） NOSQL（mongodb， redis）exit
        self.write_to_file('豆瓣电视.json')
        
    def write_to_file(self, file_name):
        """
        写入文件
        """
        path = self.file_path + file_name
        # 将列表变成字符串
        temp = {'datas': self.datas}
        # 将temp字典转换成json字符串
        temp = json.dumps(temp, ensure_ascii=False, indent=4)
        # 写入文件
        with open(path, 'w', encoding='utf-8') as f:
            f.write(temp)
        

if __name__ == '__main__':
    # 1. 首先获取tag列表
    tag_list = TVTag.get_tv_tags()
    # 2. 将列表转换成字典方便知道tag具体的值
    tag = {key: value for key, value in zip(tag_list, tag_list)}
    # 3. 创建对象
    db = DBTV(tag['英剧'])
    # 4. 启动爬虫程序
    db.run()


        