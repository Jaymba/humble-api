from shutil import which
from scrape import Scraper
from bs4 import BeautifulSoup
import re

from book import Book

    
class BundlePage(BeautifulSoup):
    
    def __init__(self, html):
        
        #with open(html, 'rb') as f:
        #    self.html = f.read()
        self.html = html

        super().__init__(self.html, 'html.parser')
        self.parse_bundle_page()


    def books_to_file(self, file_name):
        with open(file_name, 'ab') as f:
            for book in self.books:
                f.write(str(book).encode())

    def parse_bundle_page(self):

        heading = self.find('h1', 'heading-large')
        self.bundle_title = heading.img['alt'].split(':')[-1].strip()
        self.bundle_type = heading.span.string

        books = self.find_all('div', 'tier-item-details-view')
        self.books = []

        for book in books:
            self.cur_book = book
            self.books.append(Book(
                bundle_title=self.bundle_title,
                bundle_type=self.bundle_type,
                title= self.get_title(),
                author=self.get_author(),
                publisher=self.get_publisher(),
                formats=self.get_formats(),
                price=self.get_price(),
                description=self.get_description(),
                
                ))

    def get_description(self):
        description = self.cur_book.find('section','description')
        if description.p:
            return description.p.text
        else:
            return description.string
        
    def get_formats(self):
        
        formats = self.cur_book.find_all('span','fine-print')
        if formats:
            formats = formats[-1].string.replace('and', '').replace(' ','')
            return formats.split(',')
        
        return ''


    def get_publisher(self):
        publisher = ''
        divs = self.cur_book.find_all('div','publishers-and-developers')
        for div in divs:
            if 'Publisher' in div.text:
                publisher = div.text.split('\n')[-2].strip()
                break

        return publisher
                

    def get_author(self):
        author = ''
        divs = self.cur_book.find_all('div','publishers-and-developers')
        for div in divs:
            if 'Author' in div.text:
                author = div.text.split('\n')[-2].strip()
                break

        return author 

    def get_title(self):
        return self.cur_book.find('h2','heading-medium').string


    
    def get_price(self):
        string = self.cur_book.find('span', 'tier-price').string
        if(string):
            return re.search(r'\d+', string).group(0)
        return 0


class MainPage(BeautifulSoup):
    def __init__(self, html):
        self.html = html
#        with open('main.html') as f:
#            self.html = f.read()
            
        super().__init__(self.html, 'html.parser')
        self.get_bundle_urls()

    def get_bundle_urls(self):
        links = self.select('a.bundle')
        self.bundle_urls = ['https://www.humblebundle.com' + link['href'].split('?')[0] for link in links]
        
        
if __name__ == '__main__':
    scraper = Scraper(url='https://www.humblebundle.com/books/')
    main_page = MainPage(scraper.main_html)

    bundles = []
    for url in main_page.bundle_urls:
        bundle_html = scraper.scrape_bundle(url)
        bundle_page = BundlePage(bundle_html)
        books = bundle_page.books
        with open('books.txt', 'a') as f:
            [f.write(book.get_str()) for book in books]
        bundles.append(books)
