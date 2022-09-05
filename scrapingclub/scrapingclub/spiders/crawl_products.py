import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlProductsSpider(CrawlSpider):
    name = 'crawl_products'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div/h4/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[contains(text(), 'Next')]"), follow=True),
    )

    def parse_item(self, response):
        item = {}

        item['title'] = response.xpath("//h3/text()").get()
        item['price'] = response.xpath("//div[@class='card-body']/h4/text()").get()
        item['description'] = response.xpath("//p[@class='card-text']/text()").get()
        item['image'] = response.urljoin(response.xpath("//img[@class='card-img-top img-fluid']/@src").get())
        return item
