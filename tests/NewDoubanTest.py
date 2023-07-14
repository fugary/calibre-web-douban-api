import requests

from NewDouban import NewDouban

if __name__ == "__main__":
    # douban = NewDouban()
    # result = douban.search("知识考古学")
    # for book in result:
    #     print(book)

    res = requests.get('http://127.0.0.1:8083/metadata/douban_cover?cover=https%3A//img1.doubanio.com/view/subject/l/public/s29195878.jpg',
                 timeout=(10, 200), allow_redirects=False)
    print(res)
