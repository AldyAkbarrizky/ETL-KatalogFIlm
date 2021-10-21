import scrapy
from imdb.items import ImdbItem

class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?release_date=2019-09-30,2021-10-06&sort=release_date,asc']

    def parse(self, response):
        items = ImdbItem()

        movie_title = response.css(".lister-item-header > a:first-of-type::text").extract()

        items['name'] = movie_title

        yield items

        next_page = response.css(".desc > a:last-of-type::attr('href')")

        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
