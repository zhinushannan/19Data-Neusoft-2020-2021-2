import requests


class TB:
    def __init__(self, tieba_name='李毅', tieba_decode='utf-8'):
        """
        初始化方法
        :param tieba_name: 爬取的贴吧的名称，默认爬取李毅吧
        """
        # 定义请求地址
        self.url = 'https://tieba.baidu.com/f?kw=' + tieba_name + '&ie=utf-8&pn={}'
        # 定义编码
        self.tieba_decode = tieba_decode
        # 吧名
        self.name = tieba_name

    def get_requests(self, url):
        """
        发送请求并获取响应
        :param url: 发送请求的地址
        :return:
        """
        return requests.get(url=url).content.decode(self.tieba_decode)

    def save_html(self, content, page):
        """
        保存页面数据的方法
        :param content: 保存的页面内容
        :param page: 页码
        :return:
        """
        file_path = f'./tieba/{self.name}-第{page}页.txt'
        with open(file_path, 'w', encoding=self.tieba_decode) as f:
            # 写入文件
            f.write(content)

    def run(self, download_num=5):
        """
        爬虫启动程序
        :return:
        """
        # 1. 构造请求地址
        for i in range(download_num):
            # i的取值是0, 1, 2, 3, 4, 5
            url = self.url.format(i * 50)
            content = self.get_requests(url)
            self.save_html(content, i + 1)


if __name__ == '__main__':
    TB().run()
