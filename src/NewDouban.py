import random
import re
import time

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, unquote
from lxml import etree
from functools import lru_cache

from cps.services.Metadata import Metadata, MetaSourceInfo, MetaRecord

DOUBAN_SEARCH_JSON_URL = "https://www.douban.com/j/search" # 最新豆瓣屏蔽此url
DOUBAN_SEARCH_URL = "https://www.douban.com/search"
DOUBAN_BOOK_CAT = "1001"
DOUBAN_BOOK_CACHE_SIZE = 500  # 最大缓存数量
DOUBAN_CONCURRENCY_SIZE = 5  # 并发查询数
DOUBAN_BOOK_URL_PATTERN = re.compile(".*/subject/(\\d+)/?")
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}
PROVIDER_NAME = "New Douban Books"
PROVIDER_ID = "new_douban"


class NewDouban(Metadata):
    __name__ = PROVIDER_NAME
    __id__ = PROVIDER_ID

    def __init__(self):
        self.searcher = DoubanBookSearcher()
        super().__init__()

    def search(self, query: str, generic_cover: str = "", locale: str = "en"):
        if self.active:
            return self.searcher.search_books(query)


class DoubanBookSearcher:

    def __init__(self):
        self.book_loader = DoubanBookLoader()
        self.thread_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix='douban_async')

    def calc_url(self, href):
        query = urlparse(href).query
        params = {item.split('=')[0]: item.split('=')[1] for item in query.split('&')}
        url = unquote(params['url'])
        if DOUBAN_BOOK_URL_PATTERN.match(url):
            return url

    def load_book_urls_new(self, query):
        url = DOUBAN_SEARCH_URL
        params = {"cat": DOUBAN_BOOK_CAT, "q": query}
        res = requests.get(url, params, headers=DEFAULT_HEADERS)
        book_urls = []
        if res.status_code in [200, 201]:
            html = etree.HTML(res.content)
            alist = html.xpath('//a[@class="nbg"]')
            for link in alist:
                href = link.attrib['href']
                parsed = self.calc_url(href)
                if parsed:
                    if len(book_urls) < DOUBAN_CONCURRENCY_SIZE:
                        book_urls.append(parsed)
        return book_urls

    def search_books(self, query):
        book_urls = self.load_book_urls_new(query)
        books = []
        futures = [self.thread_pool.submit(self.book_loader.load_book, book_url) for book_url in book_urls]
        for future in as_completed(futures):
            book = future.result()
            if book is not None:
                books.append(future.result())
        return books


class DoubanBookLoader:

    def __init__(self):
        self.book_parser = DoubanBookHtmlParser()

    @lru_cache(maxsize=DOUBAN_BOOK_CACHE_SIZE)
    def load_book(self, url):
        book = None
        self.random_sleep()
        start_time = time.time()
        res = requests.get(url, headers=DEFAULT_HEADERS)
        if res.status_code in [200, 201]:
            print("下载书籍:{}成功,耗时{:.0f}ms".format(url, (time.time() - start_time) * 1000))
            book_detail_content = res.content
            book = self.book_parser.parse_book(url, book_detail_content.decode("utf8"))
        return book

    def random_sleep(self):
        random_sec = random.random() / 10
        print("Random sleep time {}s".format(random_sec))
        time.sleep(random_sec)

class DoubanBookHtmlParser:
    def __init__(self):
        self.id_pattern = DOUBAN_BOOK_URL_PATTERN
        self.date_pattern = re.compile("(\\d{4})-(\\d+)")
        self.tag_pattern = re.compile("criteria = '(.+)'")

    def parse_book(self, url, book_content):
        book = MetaRecord(
            id="",
            title="",
            authors=[],
            publisher="",
            description="",
            url="",
            source=MetaSourceInfo(
                id=PROVIDER_ID,
                description=PROVIDER_NAME,
                link="https://book.douban.com/"
            )
        )
        html = etree.HTML(book_content)
        title_element = html.xpath("//span[@property='v:itemreviewed']")
        book.title = self.get_text(title_element)
        share_element = html.xpath("//a[@data-url]")
        if len(share_element):
            url = share_element[0].attrib['data-url']
        book.url = url
        id_match = self.id_pattern.match(url)
        if id_match:
            book.id = id_match.group(1)
        img_element = html.xpath("//a[@class='nbg']")
        if len(img_element):
            cover = img_element[0].attrib['href']
            if not cover or cover.endswith('update_image'):
                book.cover = ''
            else:
                book.cover = cover
        rating_element = html.xpath("//strong[@property='v:average']")
        book.rating = self.get_rating(rating_element)
        elements = html.xpath("//span[@class='pl']")
        for element in elements:
            text = self.get_text(element)
            if text.startswith("作者") or text.startswith("译者"):
                book.authors.extend([self.get_text(author_element) for author_element in
                                     filter(self.author_filter, element.findall("..//a"))])
            elif text.startswith("出版社"):
                book.publisher = self.get_tail(element)
            elif text.startswith("副标题"):
                book.title = book.title + ':' + self.get_tail(element)
            elif text.startswith("出版年"):
                book.publishedDate = self.get_publish_date(self.get_tail(element))
            elif text.startswith("丛书"):
                book.series = self.get_text(element.getnext())
            elif text.startswith("ISBN"):
                book.identifiers["isbn"] = self.get_tail(element)
        summary_element = html.xpath("//div[@id='link-report']//div[@class='intro']")
        if len(summary_element):
            book.description = etree.tostring(summary_element[-1], encoding="utf8").decode("utf8").strip()
        tag_elements = html.xpath("//a[contains(@class, 'tag')]")
        if len(tag_elements):
            book.tags = [self.get_text(tag_element) for tag_element in tag_elements]
        else:
            book.tags = self.get_tags(book_content)
        return book

    def get_tags(self, book_content):
        tag_match = self.tag_pattern.findall(book_content)
        if len(tag_match):
            return [tag.replace('7:', '') for tag in
                    filter(lambda tag: tag and tag.startswith('7:'), tag_match[0].split('|'))]
        return []

    def get_publish_date(self, date_str):
        if date_str:
            date_match = self.date_pattern.fullmatch(date_str)
            if date_match:
                date_str = "{}-{}-1".format(date_match.group(1), date_match.group(2))
        return date_str

    def get_rating(self, rating_element):
        return float(self.get_text(rating_element, '0')) / 2

    def author_filter(self, a_element):
        a_href = a_element.attrib['href']
        return '/author' in a_href or '/search' in a_href

    def get_text(self, element, default_str=''):
        text = default_str
        if len(element) and element[0].text:
            text = element[0].text.strip()
        elif isinstance(element, etree._Element) and element.text:
            text = element.text.strip()
        return text if text else default_str

    def get_tail(self, element, default_str=''):
        text = default_str
        if isinstance(element, etree._Element) and element.tail:
            text = element.tail.strip()
            if not text:
                text = self.get_text(element.getnext(), default_str)
        return text if text else default_str
