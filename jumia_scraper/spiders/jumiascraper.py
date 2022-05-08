import scrapy


class JumiascraperSpider(scrapy.Spider):
    name = 'jumiascraper'
    start_urls = ['http://jumia.com.ng/catalog/?q=oraimo']

    def parse(self, response):
        for products in response.css('a.core'):
            # self.log(message=len(products))
            if(products.css('h3.name::text').get() and products.css('div.prc::text').get()):
                yield {
                    'product_name': products.css('h3.name::text').get(),
                    'product_image_url': products.css('img.img').attrib['data-src'],
                    # check if ₦ is in the price string and remove it else return the price
                    'product_price': products.css('div.prc::text').get().replace('₦', '') if '₦' in products.css('div.prc::text').get() else products.css('div.prc::text').get(),
                    'product_url': 'https://jumia.com.ng'+products.attrib['href'],
                    'product_rating': products.css('div.rev::text').get().replace('(', '').replace(')', '') if products.css('div.rev::text').get() else 0,
                }
        # last_page = response.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[2]/a[7]').attrib['href']
        # # extract page number '16' from the '/catalog/?q=oraimo&page=16#catalog-listing' and remove the '#catalog-listing'
        # # remove all characters expect "page=" and extract the number
        # page_number = last_page.split('page=')[1].split('#')[0].split('&')[0]
        # # loop throuhg the pages and yield the next page
        # for page in range(2, int(page_number)+1):
        #     next_page = f'https://jumia.com.ng/catalog/?q=oraimo&page={page}/#catalog-listing'
        #     yield response.follow(next_page, callback=self.parse)

        next_page = response.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[2]/a[6]')
        # check if next page has a href attribute
        if next_page and next_page.attrib['href']:
            next_page_url = 'https://jumia.com.ng' + next_page.attrib['href']
            yield response.follow(next_page_url, callback=self.parse)

