import crawler

if '__main__' == __name__:
    crawler = crawler.Crawler()

    #keyword_list는 그냥 넣고 싶은 키워드로 리스트 형태로 넣기
    keyword_list = []

    for keyword in keyword_list:
        crawler.search_keyword(keyword)
        crawler.scroll_down(repeat=5)
        data = crawler.get_data(keyword)
        # for d in data:
        #     worker.insert_data(d)
