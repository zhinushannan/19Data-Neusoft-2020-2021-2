import requests


# 请求地址
# 第一页
# https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=0
# 第二页
# https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=50
# 第三页
# https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=100


class TB:
    def __init__(self, tieba_name='李毅', tieba_encode='utf-8'):
        """
        初始化方法
        @program tieba_name: 爬取的贴吧的名称，默认爬取李毅吧
        """
        # 定义请求的地址
        self.url = "https://tieba.baidu.com/f?kw=" + tieba_name + "&ie=utf-8&pn={}"
        # 定义编码
        self.tieba_encode = tieba_encode
        # 保存吧名
        self.name = tieba_name

    
    def get_request(self, url):
        """
        发送请求并获取响应的
        @program url：发送请求的地址
        """
        return requests.get(url=url).content.decode(self.tieba_encode)

    
    def save_html(self, content, page):
        """
        保存页面数据的方法
        @program content: 保存的页面内容
        @program page: 页码
        """
        file_path = f'./tieba/{self.name}-第{page + 1}页.txt'
        with open(file_path, 'w', encoding=self.tieba_encode) as f:
            # 写入文件
            f.write(content)

    
    def run(self, download_num=5):
        """
        爬虫启动程序
        """
        for i in range(download_num):
            # i的取值0 1 2 3 4
            # 1. 构造请求地址
            url = self.url.format(i * 50)
            # 2. 发送请求并获取响应
            content = self.get_request(url)
            # 3. 保存页面内容
            self.save_html(content, i)


if __name__ == "__main__":
    TB(tieba_name="美女").run()
