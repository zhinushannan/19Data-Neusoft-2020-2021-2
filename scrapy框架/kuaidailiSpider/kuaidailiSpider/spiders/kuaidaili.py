import scrapy


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['http://kuaidaili.com/free']

    def parse(self, response):

        selectors = response.xpath('//tbody/tr')
        proxies = []
        for selector in selectors:
            proxy = {
                'ip': selector.xpath('./td[1]/text()').get(),
                'port': selector.xpath('./td[2]/text()').get()
            }
            print(proxy)
            proxies.append(proxy)
        pass
