from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup


def extract_news(html_doc: str, n_of_news_to_extract: int = 30) -> List[Dict[str, Any]]:
    page = BeautifulSoup(html_doc, "html.parser")
    table = page.table.findAll('table')[1]
    news = []
    items = table.findAll("tr")
    for index in range(n_of_news_to_extract):
        a = items[3 * index + 0]
        b = items[3 * index + 1]
        item = {'author': b.find(class_="subtext").find(class_="hnuser").text,
                'author_url': b.find(class_="subtext").find(class_="hnuser")['href'],
                'comments': (0 if b.find(class_="subtext").findAll("a")[-1].text == 'discuss'
                             else b.find(class_="subtext").findAll("a")[-1].text.split()[0]),
                'points': int(b.find(class_="subtext").find(class_="score").text.split()[0]),
                'title': a.findAll("td")[-1].find("a", class_="storylink").text,
                'url': a.findAll("td")[-1].find("a", class_="storylink", href=True)["href"]}
        try:
            item['resource_text'] = a.findAll("td")[-1].find("span").findChild().text
        except AttributeError:
            item['resource_text'] = None
        try:
            item['resource_url'] = a.findAll("td")[-1].find("span").findChild()['href']
        except AttributeError:
            item['resource_url'] = None

        ## TODO: add item['time']
        ## time_ago = b.find(class_="subtext").find(class_="age").text

        ## TODO: добавить обработку разделов сайта
        news.append(item)
    return news


def extract_next_page_url(html_doc: str) -> str:
    page = BeautifulSoup(html_doc, "html.parser")
    table = page.table.findAll('table')[1]
    next_page_url = table.find(class_="morelink")["href"][4:]
    return next_page_url


def get_news(url="https://news.ycombinator.com/newest", n_pages: int = 5):
    html_doc = requests.get(url).text
    news: List[Dict[str, Any]] = []
    while n_pages:
        news += extract_news(html_doc)
        next_page_url = url + extract_next_page_url(html_doc)
        html_doc = requests.get(next_page_url).text
        n_pages -= 1
    return news
