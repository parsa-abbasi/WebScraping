__author__ = "Parsa Abbasi"
__email__ = "parsa.abbasi1996@gmail.com"
__organization__ = "Quera"
__website__ = "https://parsa-abbasi.github.io/"
__version__ = "1.0.1"
__date__ = "2023-04-06"

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class BookspiderSpider(CrawlSpider):
    name = 'bookspider'
    allowed_domains = ['bidgolpublishing.com']
    start_urls = ['http://bidgolpublishing.com/Books.aspx?t=0&c=0&p=1&l=1']
    
    # The rules are used to define how the spider will find the next pages
    rules = (
        Rule(LinkExtractor(restrict_css='.pages a'), callback='parse', follow=True),
    )
    
    # The DOWNLOAD_DELAY setting specifies the minimum delay between requests,
    # while the RANDOMIZE_DOWNLOAD_DELAY setting enables a random delay factor
    # that multiplies the DOWNLOAD_DELAY by a random value between 0.5 and 1.5.
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    def parse(self, response):
        BOOK_SELECTOR = '.row .img-row a'
        TITLE_SELECTOR = '.head::text'
        URL_SELECTOR = '::attr(href)'
        
        for book in response.css(BOOK_SELECTOR):
            yield {
                'title': book.css(TITLE_SELECTOR).extract_first(),
                'url': 'http://bidgolpublishing.com/' + book.css(URL_SELECTOR).extract_first(),
            }
