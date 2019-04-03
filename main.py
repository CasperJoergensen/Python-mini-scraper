import threading
from drScraper import DrScraping as DRS
from poliScraber import PoliScraping as POS

threads = []
news_sites = list()


def start_threads(search_word: str):

    dr_scraper = DRS(search_word)
    dr_thread = threading.Thread(target=dr_scraper.scrape)
    threads.append(dr_thread)
    news_sites.append(dr_scraper)
    dr_thread.start()

    # tv2_scraper = TV2_scraper(search_word)
    # tv2_thread = threading.Thread('tv2_scraper.start')
    # threads.append(tv2_thread)
    # news_sites.append(tv2_scraper)
    # tv2_thread.start()
    
    poli_scraper = POS(search_word)
    poli_thread = threading.Thread(target=poli_scraper.scrape)
    threads.append(poli_thread)
    news_sites.append(poli_scraper)
    poli_thread.start()

def join_threads():
    for thread in threads:
        thread.join()


def merge_and_sort() -> list:
    all_articles = []
    for site in news_sites:
        all_articles += site.get_list()
    return sorted(all_articles, key=lambda k: k['time_published'], reverse=True)


def print_results(list_of_news: list):

    if len(list_of_news) > 0:
        for article in list_of_news:
            print('-' * 100)
            for k, v in article.items():
                print(f'{k if k != "href" else "Link"}: {v}')
        print('-' * 20)
    else:
        print("Ingen nyheder fundet")


if __name__ == "__main__":
    while True:
        news_sites.clear()
        search_word = input("Hvad vil du søge på? ")
        start_threads(search_word)
        join_threads()
        print_results(merge_and_sort())

