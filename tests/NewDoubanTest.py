from NewDouban import NewDouban

if __name__ == "__main__":
    douban = NewDouban()
    result = douban.search("知识考古学")
    for book in result:
        print(book)
