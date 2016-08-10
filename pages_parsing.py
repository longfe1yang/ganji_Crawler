from bs4 import BeautifulSoup
import requests
import time
import models


def formatted(string):
    return string.replace("\n", "").replace("\t", "").replace(" ", "")


def url_exist(url):
    return url in [i['url'] for i in models.second_grade.find()]


def get_links_from(channel, pages):
    list_view = '{}o{}/'.format(channel, pages)
    wb_data = requests.get(list_view)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # 判断页面是否存在，找的是<div class="pageBox">
    # 有，页面就存在，没有，页面就不存在
    if soup.find('div', 'pageBox'):
        urls = soup.select('[class=ft-tit]')
        for u in urls:
            url = u.get('href')
            # 去重判断
            if not url_exist(url):
                data = {
                    'url': url,
                    'channel': channel
                }
                print(data)
                models.second_grade.save(data)
            else:
                continue


def item_info_exist(url):
    return url in [i['url'] for i in models.third_grade.find()]


def get_item_info(url):
    if not item_info_exist(url):
        wb_data = requests.get(url)
        time.sleep(2)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        page_404_1 = soup.select('div.leftBox > div:nth-of-type(4) > div > ul > li:nth-of-type(1) > span:nth-of-type(1)')
        if len(page_404_1) == 0 and soup.find('p', 'error-tips1') is None:
            title = soup.find('h1', 'title-name').text
            tm = soup.find('i', 'pr-5').text.strip()
            typ = soup.select('div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a')[0].text
            price = soup.find('i', 'f22 fc-orange f-type').text
            p = soup.select('div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3) > a')
            place = ''
            for i in range(len(p)):
                place += p[i].get_text()
            state = soup.select('div.second-dt-bewrite > ul > li')
            data = {
                'url': url,
                'title': title,
                'time': tm,
                'type': typ,
                'price': price,
                'place': place,
                'state': formatted(state[0].get_text() if len(state) != 0 else "")
            }
            models.third_grade.save(data)
            print(data)
        else:
            pass
    else:
        pass


if __name__ == '__main__':
    get_item_info('http://bj.ganji.com/jiaju/2215310340x.htm')
