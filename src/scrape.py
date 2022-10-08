from cgitb import html
from ssl import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Scraper():
    
    def __init__(self, url):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

        self.driver.get(url)
        self.main_html = self.driver.page_source
        

    def close(self):
        self.driver.close()

    def scrape_bundle(self, url):
        self.driver.get(url)
        html = self.driver.page_source 
        return html 
    
    def scrape_bundle_pages(self, urls):
        self.bundle_htmls = []

        for url in urls:
            self.driver.get(url)
            self.bundle_htmls.append(self.driver.page_source)

        


if __name__ == '__main__':
    scrape = Scraper('https://www.humblebundle.com/books/craft-game-design-books')
    scrape.close()