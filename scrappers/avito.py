import datetime
from datetime import time
from time import sleep
import unicodedata
from bs4 import BeautifulSoup
import scrappers.scrapper as scrapper
import cloudscraper
import json
import sys
import utils.find
from utils.api.cloudflare_api import __Cloudflare as API

class Avito(scrapper.Scrapper):
    def __init__(self) -> None:
        self.name = "avito"
        # TODO: read from config
        self.ans_file = open("avito.json", "w")

    def get_links(self, params={}):
        res_links = []
        # получение урла с хешированными фильтрами
        url = API.avito_get_hashed_url(params)

        for p in range(1, 100):
            r = API.get(url, params={"p": p})
            soup = BeautifulSoup(r.text, "html.parser")
            # r = driver.get(url)
            # soup = BeautifulSoup(driver.page_source, "html.parser")

            print("page:", p)

            # for debug
            with open("avito.html", "w") as f:
                f.write(r.text)

            links = ["https://www.avito.ru" + i.get("href") for i in soup.find_all("a", "iva-item-sliderLink-uLz1v")]
            res_links += links

        return res_links


    def scrap_link(self, link):
        if not 'moskva' in link:
            return None
        sleep(3)
        r = API.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        with open("avito_moment.html", "w") as f:
            f.write(soup.prettify())
        cur_params = dict()

        cur_params["Id"] = r.url.split('/')[-1]
        cur_params["Url"] = r.url

        params = soup.find_all("li", class_="params-paramsList__item-appQw")
        for i in params:
            key, value = unicodedata.normalize("NFKD", i.get_text()).split(':')
            value = value[1:]
            cur_params[key] = value
        
        params = soup.find_all("li", class_="style-item-params-list-item-aXXql")
        for i in params:
            key, value = unicodedata.normalize("NFKD", i.text).split(':')
            value = value[1:]
            cur_params[key] = value

        params = soup.find("span", {"data-marker":"item-view/item-price"})
        # print(params)
        cur_params["Цена"] = int(unicodedata.normalize("NFKD", params.text).replace(' ', ''))

        subways = soup.find_all("span", "style-item-address-georeferences-item-TZsrp")
        subways_arr = []
        for i in subways:
            spans = i.find_all("span")
            try:
                subways_arr.append({spans[1].text: spans[2].text})
            except:
                continue
        cur_params["Метро"] = subways_arr
        
        cur_params["Просмотры"] = int(unicodedata.normalize("NFKD", soup.find("span", {"data-marker": "item-view/total-views"}).text).split(' ')[0])
        cur_params["Дата выхода"] = unicodedata.normalize("NFKD", soup.find("span", {"data-marker": "item-view/item-date"}).text)

        date = cur_params["Дата выхода"]
        try:
            arr = date.split(' ')
            if 'сегодня' in date:
                d = datetime.datetime.now()
            elif 'вчера' in date:
                d = datetime.datetime.now() - datetime.timedelta(days=1)
            elif 'позавчера' in date:
                d = datetime.datetime.now() - datetime.timedelta(days=2)
            else:
                month_arr = ['января', 'февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','декабря']
                month = month_arr.index(arr[3]) if arr[3] in month_arr else -1
                month += 1 

                year = 2023
                day = int(arr[2])
                d = datetime.date(year, month, day)
            unixtime = time.mktime(d.timetuple())
            cur_params["Дата выхода (unixtime)"] = unixtime
        except Exception as e:
            print("error with converting to unixtime: ", e, date, arr)

        params_buf = cur_params.copy()
        for key, value in params_buf.items():
            if 'площадь' in str(key).lower():
                new_key = str(key) + " (fixed)"
                cur_params[new_key] = float(value.split(' ')[0])
            if 'лифт' in str(key).lower():
                new_key = str(key) + " (fixed)"
                cur_params[new_key] = int(value.split(' ')[0])

        if "Этаж" in cur_params:
            cur_params["Этаж (fixed)"] = int(cur_params["Этаж"].split(' ')[0])
            cur_params["Всего этажей"] = int(cur_params["Этаж"].split(' ')[2])
        if "Высота потолков" in cur_params:
            cur_params["Высота потолков (fixed)"] = float(cur_params["Высота потолков"].split(' ')[0])
        if "Срок сдачи" in cur_params:
            try:
                finish_year = 0
                for i in cur_params["Срок сдачи"].split(' '):
                    if i.isnumeric():
                        finish_year = max(finish_year, int(i))
                cur_params["Срок сдачи (fixed)"] = int(finish_year)
            except:
                print("[ERROR] in 'Срок сдачи' making 'Срок сдачи (fixed)':", cur_params["Срок сдачи"])

        cur_params["Дата парсинга"] = time.mktime(datetime.datetime.now().timetuple())


        self.ans_file.write(json.dumps(cur_params)) 
        self.ans_file.write(",")

        first = False

        return {}