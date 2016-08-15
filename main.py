from multiprocessing import Pool
from pages_parsing import get_links_from
from pages_parsing import get_item_info
from channels import get_index_url
import models


def get_all_links_from(channel):
    for i in range(1, 100):
        get_links_from(channel, i)


# 这个get_index_url写了去重功能，也就是说
# 这个get_start()运行无论多少次，都不会加入重复信息
def get_start():
    start_url = 'http://bj.ganji.com/wu/'
    host = 'http://bj.ganji.com'
    get_index_url(start_url, host)


# 从二级拿出数据和三级（详细页面）中所有url对比，给出来剩下没有爬取的
# 详细页面url
def info_rst():
    all_url = [i['url'] for i in models.second_grade.find()]
    exist_url = [i['url'] for i in models.third_grade.find()]
    return set(all_url) - set(exist_url)


# 从一级索引拿出page_url和二级索引做对比，给出来一级下面没有爬取的
def url_rst():
    page_url = [i['page_url'] for i in models.first_grade.find()]
    exist_page_url = [i['channel'] for i in models.second_grade.find()]
    return set(page_url) - set(exist_page_url)


def main():
    get_start()
    pool = Pool(processes=4)
    pool.map(get_all_links_from, url_rst())
    pool.map(get_item_info, info_rst())
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
