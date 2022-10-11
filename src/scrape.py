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
    

    def updated_list(self):
        self.get_bundle_titles()
        cur_titles = self.load_json('books.json')
        
        new_titles = list(set(self.current_bundle_titles).symmetric_difference(set(cur_titles)))

        if(new_titles):
            return new_titles
        else:
            return False

    def get_bundle_titles(self):
        sections = self.home_page_html.find_all('div', 'info-section')
        self.current_bundle_titles = []
        for section in sections:
            title = section.find('span', 'name').string
            title = title.split(':')[-1].strip()
            self.current_bundle_titles.append(title)

    def load_json(self, file_name):

        with open(file_name, 'r') as f:
            bundles = json.load(f)    
        return bundles

    
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
    scrape.get_bundle_titles()
#    scrape.scrape_bundle_pages()
#    scrape.parse_bundle_pages()
#    scrape.write_to_file()
    
    with open('books.json', 'r') as f:
        bundles = json.load(f)

    print(list(set(scrape.current_bundle_titles).symmetric_difference(set(bundles.keys()))))

    

