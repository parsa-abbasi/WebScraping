import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['bidgolpublishing.com']
    start_urls = ['http://bidgolpublishing.com/Books.aspx?t=0&c=0&p=1&l=1']

    def parse(self, response):
        BOOK_SELECTOR = '.row .img-row a'
        TITLE_SELECTOR = '.head::text'
        URL_SELECTOR = '::attr(href)'
        
        for book in response.css(BOOK_SELECTOR):
            yield {
                'title': book.css(TITLE_SELECTOR).extract_first(),
                'url': 'http://bidgolpublishing.com/' + book.css(URL_SELECTOR).extract_first(),
            }
        
        splitted = response.url.split('p=')
        p_l = splitted[1].split('&')
        current_page = p_l[0]
        next_page_number = int(current_page) + 1
        
        last_item = response.css('.pages a::attr(id)').getall()[-1]
        if last_item[0] == 'p':
            last_page_number = last_item.split('_')[1]
            if last_page_number == current_page:
                return
        else:
            next_page_url = splitted[0] + 'p=' + str(next_page_number) + '&' + p_l[1] 
            yield scrapy.Request(next_page_url)
