import requests
import json


class TXZP:
    def __init__(self):
        # 请求地址（岗位列表）
        self.url = "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1621650356179&parentCategoryId=40001&pageIndex={}&pageSize=10&language=zh-cn&area=cn"
        # 请求头
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        # 定义数据源
        self.datas = []
    
    def get_response(self, url):
        """
        发送请求并获取响应
        """
        return requests.get(url=url, headers=self.header).content.decode()

    def parse_list_data(self, data):
        """
        解析列表页数据
        """
        # 转换
        job_info = json.loads(data)
        # 提取要保存的数据
        for j in job_info['Data']['Posts']:
            # 创建数据字典存储将要写入文件的数据
            job = {}
            # 保存岗位名称
            job['job_name'] = j['RecruitPostName']
            # 保存岗位地点
            job['job_loc'] = j['LocationName']
            # 保存岗位的发布时间
            job['job_time'] = j['LastUpdateTime']
            # 保存岗位的性质
            job['job_type'] = j['CategoryName']
            # 保存岗位的工作职责
            job['job_responsibility'] = j['Responsibility']
            # 根据岗位id拼接岗位的详情地址
            job_detail_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1621651952320&postId=" + j['PostId'] + "&language=zh-cn"
            # 解析二级页面内容
            self.parse_detail_data(job_detail_url, job)

    def parse_detail_data(self, url, job):
        """
        解析详情页数据
        """
        data = self.get_response(url)
        # # 根据详情地址继续发送请求获取详情页数据
        data = json.loads(data)
        # # 获取工作要求
        job['job_requirement'] = data['Data']['Requirement']
        # # 将存储好的工作放入数据源中
        self.datas.append(job)

    def run(self, page=5):
        """
        爬虫启动程序
        """
        for index in range(1, page):
            # 1. 构造地址
            url = self.url.format(index)
            # 2. 发送请求
            content = self.get_response(url)
            # 3. 解析数据
            self.parse_list_data(content)
        print(self.datas)
        

if __name__ == '__main__':
    print("=" * 100)
    TXZP().run()
