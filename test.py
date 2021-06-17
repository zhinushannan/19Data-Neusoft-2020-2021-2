import requests

from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
}
html = etree.HTML(requests.get(url='http://lishi.tianqi.com/', headers=headers).content,
                  parser=etree.HTMLParser(encoding='utf-8'))
html = html.xpath('/html/body/div[10]/div[4]/table/tbody/tr[2]')[0]
html = etree.tostring(html, encoding='utf-8').decode()
print(html)

