from multiprocessing import Pool
from pages_parsing import get_links_from
from pages_parsing import get_item_info
from channels import get_index_url
import models


def get_all_links_from(channel):
    for i in range(1, 100):
        get_links_from(channel, i)


# 这个get_index_url有去重功能
def get_start():
    start_url = 'http://bj.ganji.com/wu/'
    host = 'http://bj.ganji.com'
    get_index_url(start_url, host)


all_url = [i['url'] for i in models.second_grade.find()]
exist_url = [i['url'] for i in models.third_grade.find()]
rst_urls = set(all_url) - set(exist_url)


def main():
    # get_start()
    pool = Pool()
    all_channel = [i['page_url'] for i in models.first_grade.find()]
    # pool.map(get_all_links_from, all_channel)
    pool.map(get_item_info, rst_urls)
    pool.close()
    pool.join()
    # print(all_channel)

if __name__ == '__main__':
    main()
