import scrapy
import logging


class LaptopsSpider(scrapy.Spider):
    name = "laptops"

    def __init__(self, links_file='./links.txt', **kwargs):
        super().__init__(**kwargs)
        self.links_file = links_file

    def start_requests(self):
        links = open(self.links_file)
        urls = links.readlines()
        for i in range(len(urls)):
            if i > 0 and i % 50 == 0:
                self.log(f'crawled {i} pages', level=logging.INFO)
            yield scrapy.Request(
                url=urls[i],
            )

    def parse(self, response):

        result = {
            'title': response.css('.name h1::text').get(),
        }

        price = response.css('.price_text div::text').get()
        if not price or 'دیگر' in price:
            price = response.css('.jsx-63b317fab2efbae.buy_box_text:nth-child(2)::text').get()
        result['price'] = price

        for detail in response.css('div.jsx-5b5c456cc255c2dc.header ~ div.jsx-5b5c456cc255c2dc'):
            feature = detail.css('.detail-title::text').get()
            value = detail.css('.detail-value::text').get()
            result[feature] = value

        yield result
