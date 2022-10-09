from urllib import request
from flask import Flask
from scrape import Scraper
from bundle_page import MainPage, BundlePages
app = Flask(__name__)

    

@app.get('/current_bundles')
def get_current_bundles():
    bundles = scrape_bundles()

    return bundles 
    
def scrape_bundles():
    scraper = Scraper(url='https://www.humblebundle.com/books/')
    main_page = MainPage(scraper.main_html)
#    bundles = []
    scraper.scrape_bundle_pages(main_page.bundle_urls)
    bundle_pages = scraper.bundle_htmls
    bundles = BundlePages(bundle_pages)
    return bundles.bundles

scrape_bundles()