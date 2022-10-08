from urllib import request
from flask import Flask

app = Flask(__name__)


in_memory_datastore = {
   "COBOL": {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   "ALGOL": {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   "APL": {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
   "BASIC": {"name": "BASIC", "publication_year": 1964, "contribution": "runtime interpretation, office tooling"},
   "PL": {"name": "PL", "publication_year": 1966, "contribution": "constants, function overloading, pointers"},
   "SIMULA67": {"name": "SIMULA67", "publication_year": 1967,
                "contribution": "class/object split, subclassing, protected attributes"},
   "Pascal": {"name": "Pascal", "publication_year": 1970,
              "contribution": "modern unary, binary, and assignment operator syntax expectations"},
   "CLU": {"name": "CLU", "publication_year": 1975,
           "contribution": "iterators, abstract data types, generics, checked exceptions"},
}    

@app.get('/prog_langs')
def list_programming_languages():
    return {"programming_languages":list(in_memory_datastore.values())}
    

@app.get('/prog_langs/<prog_lang_name>')
def get_programming_language_name(prog_lang_name):
    return in_memory_datastore[prog_lang_name]

@app.get('/prog_langs_filter')
def list_prog_langs():
    try:
        before_year = request.args.get('before_year') or '30000'
        after_year = request.args.get('after_year') or '0'
    except(AttributeError):
        print('Hello World')
        before_year = '30000'
        after_year = '0'


    filter(
        lambda pl: int(before_year) > pl['publication_year'] > int(after_year),
        in_memory_datastore.values()
    )
