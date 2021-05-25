import requests
import json

from requests.models import to_key_val_list


# 请求地址
# https://movie.douban.com/j/search_subjects?type=tv&tag='美剧'&sort=recommend&page_limit=20&page_start=0


# 请求参数
# 用get请求模拟提交表单
# www.baidu.com

# get请求明文传输
# account = 'zhangsan'
# psd = '123456'

# http://www.baidu.com?account='zhangsan'&psd='123456'


# 定义url
url = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0"
# 发送请求并获取响应
# response = requests.get(url=url)
# # 输出返回的json
# print(f"json：\n{response.content.decode()}")
# print(f"豆瓣服务器是否响应我们的请求：{response.status_code}")

# 这里没有响应成功的原因是豆瓣服务器要验证我们的请求头
# 在请求中request （状态行 + 请求头 + 请求体）
# 在请求头中 User-Agent

# 改进我们在发送请求的时候需要携带请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Referer": "https://movie.douban.com/tv/",
    "Host": "movie.douban.com",
    "Cookie": "bid=ovpNEggHwoE; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1621415909%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DTFpbYaa0DNF_2qtDin5jYYkg8Ng44K2Z1cfSH7kvuzIqUUqQmIo-n5FVJSbApbkx%26wd%3D%26eqid%3Dca7f48e500031df60000000460a4d804%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1142785759.1621415909.1621415909.1621415909.1; __utmb=30149280.0.10.1621415909; __utmc=30149280; __utmz=30149280.1621415909.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.2104573480.1621415909.1621415909.1621415909.1; __utmb=223695111.0.10.1621415909; __utmc=223695111; __utmz=223695111.1621415909.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __yadk_uid=Qa6BE1AqxwQfPsFbAImjmNZHl21b4y6u; _pk_id.100001.4cf6=8c1812b35b624f3c.1621415909.1.1621416443.1621415909."
}
# 发送请求
response = requests.get(url=url, headers=header)
# 验证是否响应成功
# print(f"是否响应成功：{response.status_code}")

# 保存内容
content = response.content.decode()
# 转换
content = json.loads(content)
# 数据源
datas = []
# 提取电视剧名称和评分
for t in content["subjects"]:
    # 定义字典用来保存提取的电视信息
    tv = {}
    # 获取电视剧名称
    tv['name'] = t['title']
    # 获取电视剧的评分
    tv['rate'] = t['rate']
    # 每处理一个电视剧就将结果拼接到数据源中
    datas.append(tv)

print(datas)
