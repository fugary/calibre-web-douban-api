import requests

from cps.services.Metadata import Metadata


class Douban(Metadata):
    __name__ = "Douban Books"
    __id__ = "douban"
    doubanUrl = "http://YOUR_NAS_IP:8085"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36'
    }

    def search(self, query, generic_cover=""):
        if self.active:
            val = list()
            result = requests.get(self.doubanUrl + "/v2/book/search?q=" + query.replace(" ", "+"), headers=self.headers)
            for r in result.json()['books']:
                v = dict()
                v['id'] = r['id']
                v['title'] = r['title']
                v['authors'] = r.get('authors', [])
                v['description'] = r.get('summary', "")
                v['publisher'] = r.get('publisher', "")
                v['publishedDate'] = r.get('pubdate', "")
                v['tags'] = [tag.get('name', '') for tag in r.get('tags', [])]
                v['rating'] = r['rating'].get('average', 0)
                if r.get('image'):
                    v['cover'] = r.get('image')
                else:
                    v['cover'] = generic_cover
                v['source'] = {
                    "id": self.__id__,
                    "description": self.__name__,
                    "link": "https://book.douban.com/"
                }
                v['url'] = "https://book.douban.com/subject/" + r['id']
                val.append(v)
            return val
