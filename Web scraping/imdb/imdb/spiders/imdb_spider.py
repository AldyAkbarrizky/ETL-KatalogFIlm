import scrapy
from imdb.items import ImdbItem

class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?release_date=2019-09-30,2021-10-06&sort=release_date,asc']

    def parse(self, response):
        items = ImdbItem()

        movie_title = response.css(".lister-item-header > a:first-of-type::text").extract()
        movie_type= response.css(".genre::text").extract()
        movie_year = response.css(".unbold:nth-child(3)::text").extract()
        movie_cert = response.css(".ratings-imdb-rating strong::text").extract()
        movie_dur = response.css(".runtime::text").extract()

        items['name'] = movie_title
        items['type'] = movie_type
        items['year'] = movie_year
        items['cert'] = movie_cert/2
        items['dur'] = movie_dur
        

        yield items

        next_page = response.css(".desc > a:last-of-type::attr('href')")

        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
