import scrapy


class ScrapeProductsSpider(scrapy.Spider):
    name = 'scrape_products'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic/']

    def parse(self, response):
        products = response.xpath("//div[@class='card']")

        for product in products:
            title = product.xpath(".//div[@class='card-body']/h4/a/text()").get()
            price = product.xpath(".//div[@class='card-body']/h5/text()").get()
            # description = product.xpath()
            image = response.urljoin(product.xpath(".//a/img/@src").get())

            yield{
                'title': title,
                'price': price,
                # 'description': description,
                'image': image,
            }

        next_page = response.xpath("//a[contains(text(), 'Next')]")
        print(f"Следующая страница: {next_page}")
        if next_page:

            next_page_url = response.urljoin(next_page.xpath(".//@href").get())
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse
            )
