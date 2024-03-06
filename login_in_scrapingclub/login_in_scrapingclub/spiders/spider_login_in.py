import scrapy
from scrapy import FormRequest

class SpiderLoginInSpider(scrapy.Spider):
    name = 'spider_login_in'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/basic_login']

    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrfmiddlewaretoken']/@value").get()

        yield FormRequest.from_response(
            response,
            formxpath="//form",
            formdata={
                'name': 'scrapingclub',
                'password': 'scrapingclub',
                'csrfmiddlewaretoken': csrf_token
            },
            callback=self.after_login
        )

    def after_login(self, response):
        quote = response.xpath("//div[@class='row']")

        yield {
            print(quote.xpath(".//div[@class='mt-4 my-4']/p/text()").get()),  # вывожу в терминал
            # 'quote': quote.xpath(".//div[@class='mt-4 my-4']/p/text()").get()
        }
