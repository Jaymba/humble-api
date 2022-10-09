class Book():
    def __init__(self, title='', author='', publisher='', formats=[], price=0,edition='',description='',bundle_title='', bundle_type=''):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.formats = formats
        self.price = price

        self.bundle_title = bundle_title
        self.bundle_type = bundle_type

        self.description = description

    
    

    
    def __str__(self):
        return f'''
        Title: {self.title}
        Author: {self.author}
        Publisher: {self.publisher}
        Price: ${self.price}
        Edition: {self.edition}
        Formats: {self.formats}
        Bundle Title: {self.bundle_title}
        Bundle Type: {self.bundle_type}
        Descriptions: {self.description}'''

    def get_str(self):
        return f'''
        Title: {self.title}
        Author: {self.author}
        Publisher: {self.publisher}
        Price: ${self.price}
        Edition: {self.edition}
        Formats: {self.formats}
        Bundle Title: {self.bundle_title}
        Bundle Type: {self.bundle_type}
        Descriptions: {self.description}
        
        '''




if __name__ == '__main__':
    book = Book(title="Test",bundle='The Ultimate Bundle', author='Jay Stolt', publisher='Print House', formats=['PDF', 'EPUB', 'MOBI'], price=18, edition='1st Edition', description='This is for testing purposes')
    print(book)
    