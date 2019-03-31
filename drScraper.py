import concurrent.futures
import requests
from bs4 import BeautifulSoup


class DrScraping:
    def __init__(self, search_word: str):
        self.search_word = search_word.lower()
        self.articles = []

    def scrape(self):
        soup = BeautifulSoup(self.get_page('http://www.dr.dk'), "html.parser")
        links = soup.find_all('a')
        for link in links:
            for div in link.find_all('div'):
                try:
                    if div['class'][0] == "dredition-item-header" and len(
                            set(div.get_text().lower().split()) & set(self.search_word.split())) >= len(
                            self.search_word.split()) * (1 / 2):
                        self.articles.append({"title": div.get_text().strip().replace('  ', '. '), "href": link['href']})
                except KeyError:
                    pass

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.get_timestamp, self.articles)

    def get_timestamp(self, article):
        soup = BeautifulSoup(self.get_page(article['href']), "html.parser")
        datetime = soup.find('time')['datetime']
        article.update({"time_published": datetime})

    def get_list(self):
        return self.articles

    def get_page(self, url):
        return requests.get(url).text
