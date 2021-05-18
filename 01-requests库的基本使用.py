import requests

response = requests.get('http://www.baidu.com/')

code = response.status_code
content = response.content.decode()
print(content)
print(code)
print(response.request)
print(response.headers)
