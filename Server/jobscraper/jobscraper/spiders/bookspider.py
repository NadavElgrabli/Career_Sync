import scrapy
import re



import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    
    def __init__(self, *args, **kwargs):
        super(BookspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get("start_url", "https://www.jobisjob.com/m/company+car+provided/vacancies")]
        self.keywords = [kw.lower() for kw in kwargs.get("keywords", [])]

    def parse(self, response):
        jobs_ul = response.css("ul.list2")
        jobs = jobs_ul.css("li")
        for job in jobs:
            title = job.css("span.title::text").get()
            description_link = job.css("a.item").attrib.get("href", None)
            if title and description_link and any(keyword in title.lower() for keyword in self.keywords):
                yield {
                    "title": title,
                    "link": description_link
                }













# class BookspiderSpider(scrapy.Spider):
#     name = "bookspider"
#     allowed_domains = ["books.toscrape.com"]
#     start_urls = ["https://books.toscrape.com"]
    
    
#     def parse(self, response):
#         books = response.css("article.product_pod")

#         for book in books:
#             relative_url = book.css("h3 a").attrib["href"]
            
#             if 'catalogue/' in relative_url:
#                 absolute_url = "https://books.toscrape.com/" + relative_url
#             else:
#                 absolute_url = "https://books.toscrape.com/catalogue/" + relative_url
                
#             yield response.follow(absolute_url, callback = self.parse_book)
            
#         next_page = response.css("li.next a").attrib["href"]
        
#         if next_page is not None:
            
#             if 'catalogue/' in next_page:
#                 next_page_url = "https://books.toscrape.com/" + next_page
#             else:
#                 next_page_url = "https://books.toscrape.com/catalogue/" + next_page
                
#             yield response.follow(next_page_url, callback = self.parse)

#     def parse_book(self, response):
#         prod = response.css("article.product_page")
#         stock_num = "".join(re.findall(r'\d+', response.css("p.instock.availability::text").getall()[1]))
        
#         yield {
#             "title": prod.css("h1::text").get(),
#             "price": prod.css("p.price_color::text").get(),
#             "stock": stock_num,
#             "url": response.url,
#             "Product Type": response.css("table.table tr:nth-child(2) td::text").get(),
#         }
