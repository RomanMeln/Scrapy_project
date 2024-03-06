import scrapy
from scrapy_splash import SplashRequest


class ScrapyLesson6Spider(scrapy.Spider):
    name = 'scrapy_lesson_6'
    allowed_domains = ['scrapingclub.com']
    # start_urls = ['https://scrapingclub.com/exercise/detail_sign/']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(1))
            return {
                html = splash:html()
            }
        end         
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://scrapingclub.com/exercise/detail_sign/',    # указываем ссылку на сайт, который хотим спарсить
            callback=self.parse,    # после выполнения скрипта передаем ответ в функцию parse
            endpoint='execute',    # выполнить скрипт
            args={
                'lua_source': self.script    # указываем, какой скрипт выполнить
            }
        )

    def parse(self, response):
        # print(response)
        products = response.xpath("//div[@class='row']")
        # print(products)
        for product in products:
            yield {
                'image': response.urljoin(product.xpath("//img[@class='card-img-top img-fluid']/@src").get()),
                'title': product.xpath("//div[@class='card-body']/h4[@class='card-title']/text()").get(),
                'price': product.xpath("//div[@class='card-body']/h4[@class='card-price']/text()").get(),
                'description': product.xpath("//div[@class='card-body']/p[@class='card-description']/text()").get()
            }
