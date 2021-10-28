from douban import Douban

if __name__ == "__main__":
    douban = Douban()
    result = douban.search('人民的名义')
    for book in result:
        print(book.get('title'), book.get('url'))
