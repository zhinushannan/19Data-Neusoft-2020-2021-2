import requests


# 1. 确认一下发送的地址
url = "http://www.baidu.com"

# 2. 发送请求并接收响应
response = requests.get(url=url)

# 3. 验证服务器是否有响应
print(f"从百度服务器返回的状态码是{response.status_code}")

# 4. 从响应中获取响应体内容
# print(response.content)
# print(response.content.decode())
# print(response.text)

# 5. 获取响应头
print(f"获取的响应头：{response.headers}")

# 6. 获取请求
print(f"获取请求：{response.request}")