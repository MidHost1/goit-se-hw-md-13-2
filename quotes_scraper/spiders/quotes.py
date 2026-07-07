import scrapy
from quotes.documents import Author, Quote

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author_name = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            author, _ = Author.objects.get_or_create(fullname=author_name)
            Quote.objects.get_or_create(text=text, author=author, tags=tags)
            
            yield {'text': text, 'author': author_name}

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)