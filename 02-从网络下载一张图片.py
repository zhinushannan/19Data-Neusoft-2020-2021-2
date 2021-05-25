import requests


# 1. 定义url（请求的地址）
img_url = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fyouimg1.c-ctrip.com%2Ftarget%2Ftg%2F035%2F063%2F726%2F3ea4031f045945e1843ae5156749d64c.jpg&refer=http%3A%2F%2Fyouimg1.c-ctrip.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1623917361&t=9dd02d301f43c8fa52522f1704dfae07"

# 2. 发送http请求获取数据
response = requests.get(url=img_url)

# 3. 保存图片的字节
img_bytes = response.content

# 4. 保存图片到本地
# 4.1 定义图片的保存地址
file_path = './图片.jpg'
with open(file_path, 'wb') as f:
    f.write(img_bytes)


