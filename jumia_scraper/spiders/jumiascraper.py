import scrapy


class JumiascraperSpider(scrapy.Spider):
    name = 'jumiascraper'
    start_urls = ['http://jumia.com.ng/catalog/?q=oraimo']

    def parse(self, response):
        for products in response.css('a.core'):
            self.log(message=len(products))
            if(products.css('h3.name::text').get() and products.css('div.prc::text').get()):
                yield {
                    'product_name': products.css('h3.name::text').get(),
                    'product_image_url': products.css('img.img').attrib['data-src'],
                    'product_price': products.css('div.prc::text').get(),
                    'product_url': 'https://jumia.com.ng'+products.attrib['href'],
                    # 'product_rating': products.css('div.rev::text').get().replace('(', '').replace(')', '')
                }
        # response xpath for pagination
        next_page = 'https://jumia.com.ng'+response.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[2]/a[6]').attrib['href']
        if next_page:
            yield response.follow(next_page, callback=self.parse)

