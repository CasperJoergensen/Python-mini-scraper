import requests
import re
import concurrent.futures

class PoliScraping:
    
    def __init__(self, search_word: str):
        self.search_word = search_word.lower()
        self.articles = []

    def scrape(self):
        front_page = self.get_page('http://politiken.dk')
        for m in re.finditer(r"list-item__title headline headline--xxsma", front_page):
            text = front_page[m.start()-500:m.end()+500]
            text = text[[m.start() for m in re.finditer('<a', text[:-500])][-1]: ]
            text = text[ :re.search('</a>', text).start()]
            if self.search_word in text:
                href = text[re.search('href=\"', text).end(): ]
                href = href[ :re.search('\"', href).start()]
                if 'politiken.dk' not in href:
                    continue
                title = text[re.search("<h3.*?>", text).end(): ]
                title = title[ :re.search('</h3>',title).start()]
                title = re.sub('<.*?>','', title).strip()
                article = {"title": title, "href": href}
                if article not in self.articles:
                    self.articles.append(article)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.get_timestamp, self.articles)

    def get_timestamp(self, article):
        page = get_page(article['href'])
        datetime = re.search('<meta property="article:published_time" content=".*?>',page)
        datetime = page[datetime.start()+49:datetime.end()-4]
        article.update({"time_published": datetime})   
        
    def get_list(self):
        return self.articles
    
    def get_page(self, url):
        return requests.get(url).text.lower()
