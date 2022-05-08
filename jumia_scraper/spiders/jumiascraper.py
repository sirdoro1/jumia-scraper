import scrapy


class JumiascraperSpider(scrapy.Spider):
    name = 'jumiascraper'
    allowed_domains = ['jumia.com.ng']
    start_urls = ['http://jumia.com.ng/']

    def parse(self, response):
        pass
