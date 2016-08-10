from bs4 import BeautifulSoup
import requests
import models
import time


def page_url_exist(page_url):
    return page_url in [i['page_url'] for i in models.first_grade.find()]


# 最大化利用一致性
def get_index_url(url, host):
    res = requests.get(url)
    time.sleep(2)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    titles = soup.select('#wrapper > div.content > div > div > dl.fenlei > dt > a')
    for i in titles:
        title = i.get_text()
        url = i.get('href')
        page_url = host + url
        if not page_url_exist(page_url):
            data = {
                'title': title,
                'page_url': page_url
            }
            models.first_grade.save(data)
            print(data)
        else:
            continue


if __name__ == '__main__':
    start_url = 'http://bj.ganji.com/wu/'
    host = 'http://bj.ganji.com'
    get_index_url(start_url)
