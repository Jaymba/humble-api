from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json


class Scraper():
    home_page = 'https://www.humblebundle.com/books'
    bundles = {}
    
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.home_page)
        self.home_page_html = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.driver.close

        self.get_bundle_urls() 

    
    def scrape_bundle_pages(self):
        self.bundle_htmls = []

        for url in self.bundle_urls:
            self.driver.get(url)
            self.bundle_htmls.append(self.driver.page_source)
        
    
    def get_bundle_urls(self):
        links = self.home_page_html.select('a.bundle')
        self.bundle_urls = ['https://www.humblebundle.com' + link['href'].split('?')[0] for link in links]

    
    def parse_bundle_pages(self):
        for bundle_html in self.bundle_htmls:
            self.parse_bundle_page(bundle_html)


    def parse_bundle_page(self,html):
        bs = BeautifulSoup(html,'html.parser')

        heading = bs.find('h1', 'heading-large')
        bundle_title = heading.img['alt'].split(':')[-1].strip()
        bundle_type = heading.span.string

        book_sections = bs.find_all('div', 'tier-item-details-view')
        books = {} 

        for section in book_sections:
            #self.cur_book = section 
            book = {self.get_title(section):{
                    'Author': self.get_author(section),
                    'Publisher':self.get_publisher(section),
                    'Formats':self.get_formats(section),
                    'Price':self.get_price(section),
                    'Description':self.get_description(section)}}

            books.update(book)
            
        books.update({'Bundle Type': bundle_type})

        self.bundles[bundle_title] = books
        

    def books_to_file(self, file_name):
        with open(file_name, 'ab') as f:
            for book in self.books:
                f.write(str(book).encode())


    def get_description(self,html):
        description = html.find('section','description')
        if description.p:
            return description.p.text
        else:
            return description.string
        
    def get_formats(self,html):
        
        formats = html.find_all('span','fine-print')
        if formats:
            formats = formats[-1].string.replace('and', '').replace(' ','')
            return formats.split(',')
        
        return ''


    def get_publisher(self,html):
        publisher = ''
        divs = html.find_all('div','publishers-and-developers')
        for div in divs:
            if 'Publisher' in div.text:
                publisher = div.text.split('\n')[-2].strip()
                break

        return publisher
                

    def get_author(self,html):
        author = ''
        divs = html.find_all('div','publishers-and-developers')
        for div in divs:
            if 'Author' in div.text:
                author = div.text.split('\n')[-2].strip()
                break

        return author 

    def get_title(self,html):
        return html.find('h2','heading-medium').string


    
    def get_price(self,html):
        string = html.find('span', 'tier-price').string
        if(string):
            return re.search(r'\d+', string).group(0)
        return 0

    def write_to_file(self, file_name='books.json'):
        with open(file_name,'w') as f:
            json.dump(self.bundles, f, indent=4)




if __name__ == '__main__':
    scrape = Scraper()
    scrape.scrape_bundle_pages()
    scrape.parse_bundle_pages()
    scrape.write_to_file()

    