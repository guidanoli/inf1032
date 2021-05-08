# Downloads all data from CEDAE to the pdf/ folder

import urllib.request
import urllib.parse
import os.path
from html.parser import HTMLParser

CEDAE_page_URL = 'https://cedae.com.br/relatoriosguandu'
CEDAE_page_encoding = 'utf8'
CEDAE_page_keywords = ['GEOSMINA']
CEDAE_pdf_output_dir = 'pdf'

print('Requesting \'%s\'' % CEDAE_page_URL)
with urllib.request.urlopen(CEDAE_page_URL) as fp:
    CEDAE_data_bytes = fp.read()

print('Decoding HTML to \'%s\' encoding' % CEDAE_page_encoding)
CEDAE_data_Unicode = CEDAE_data_bytes.decode(CEDAE_page_encoding)

class URLScrapper(HTMLParser):
    def __init__(self, keywords):
        super().__init__()
        self.a = False
        self.URL = None
        self.URLs = []
        self.keywords = keywords

    def get_URLs(self):
        return self.URLs

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.a = True
            for name, value in attrs:
                if name == 'href':
                    self.URL = value
                    break

    def handle_data(self, data):
        if self.a and self.URL:
            for keyword in self.keywords:
                if keyword in data:
                    self.URLs.append(self.URL)
                    break

    def handle_endtag(self, tag):
        if tag == 'a':
            self.a = False
            self.URL = None

scrapper = URLScrapper(CEDAE_page_keywords)
print('Scrapping URLs from HTML')
scrapper.feed(CEDAE_data_Unicode)
scrapped_URLs = scrapper.get_URLs()

try:
    os.mkdir(CEDAE_pdf_output_dir)
except FileExistsError:
    pass

print('%d URLs scrapped' % len(scrapped_URLs))
for scrapped_URL in scrapped_URLs:
    scrapped_URL = scrapped_URL.replace(' ', '%20')
    print('Requesting \'%s\'' % scrapped_URL)
    with urllib.request.urlopen(scrapped_URL) as infp:
        parsed_URL = urllib.parse.urlparse(scrapped_URL)
        filename = os.path.basename(parsed_URL.path).replace('%20', ' ')
        filepath = os.path.sep.join([CEDAE_pdf_output_dir, filename])
        print('Writing to \'%s\'' % filepath)
        with open(filepath, 'wb') as outfp:
            outfp.write(infp.read())
