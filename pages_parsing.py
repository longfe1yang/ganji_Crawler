from bs4 import BeautifulSoup
import requests
import time
import models


def formatted(string):
    return string.replace("\n", "").replace("\t", "").replace(" ", "")


def url_save(url, channel):
    urls = [i['url'] for i in models.second_grade.find()]
    if url not in urls:
        data = {
            'url': url,
            'channel': channel
        }
        print(data)
        models.second_grade.save(data)
    else:
        return None


def get_links_from(channel, pages):
    list_view = '{}o{}/'.format(channel, pages)
    wb_data = requests.get(list_view)
    time.sleep(2)
    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # 判断页面是否存在，找的是<div class="pageBox">
        # 有，页面就存在，没有，页面就不存在
        if soup.find('div', 'pageBox'):
            urls = soup.select('[class=ft-tit]')
            for u in urls:
                url = u.get('href')
                url_save(url, channel)
        else:
            return


def item_info_exist(url):
    return url in [i['url'] for i in models.third_grade.find()]


def info_page_exist(soup):
    page_404_1 = soup.select('div.leftBox > div:nth-of-type(4) > div > ul > li:nth-of-type(1) > span:nth-of-type(1)')
    return len(page_404_1) == 0 and soup.find('p', 'error-tips1') is None


def get_item_info(url):
    if not item_info_exist(url):
        wb_data = requests.get(url)
        if wb_data.status_code != 200:
            return None
        time.sleep(2)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if info_page_exist(soup):
            tm = soup.select('.pr-5')
            cate = soup.select('div.h-crumbs > div > a')
            price = soup.select('.f22.fc-orange.f-type')
            place = soup.select('ul.det-infor > li:nth-of-type(3) > a')
            state = soup.select('div.second-dt-bewrite > ul > li')
            data = {
                'url': url,
                'title': soup.title.text.strip(),
                'time': tm[0].text.strip().split(' ')[0] if len(tm) > 0 else "",
                'cate': [cate.text.strip() for cate in cate],
                # 'cate': cate[0].get_text(),
                'price': price[0].text.strip() if len(price) > 0 else 0,
                'place': [area.text.strip() for area in place if area.text.strip() != "-"],
                'state': formatted(state[0].get_text() if len(state) != 0 else "")
            }
            models.third_grade.save(data)
            print(data)
        else:
            pass
    else:
        pass


if __name__ == '__main__':
    get_item_info('http://bj.ganji.com/ruanjiantushu/2109678197x.htm')
