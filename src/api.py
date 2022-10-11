from flask import Flask
from scrape import Scraper

app = Flask(__name__)

    

@app.get('/current_bundles')
def get_current_bundles():
    bundles = scrape_bundles()

    return bundles 

@app.get('/user')
def new_user():
    pass
    
def scrape_bundles():

    scrape = Scraper()
    scrape.scrape_bundle_pages()
    scrape.parse_bundle_pages()
    return scrape.bundles
