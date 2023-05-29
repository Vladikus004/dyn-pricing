import cloudscraper
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import unicodedata
import datetime
import json

from utils import csv_writer

# url = "https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?f=ASgBAQICAUSSA8YQAUCQvg0Ukq41"
# url = "https://www.avito.ru/moskva/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?f=ASgBAQICAUSSA8YQAkDmBxSOUpC~DRSSrjU"

url = "https://www.avito.ru/moskva/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?f=ASgBAQICAUSSA8YQAkDmBxSOUpC~DRSSrjU"

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }
)

problem_links = []

# driver = webdriver.Firefox()
result = []
first = True
step = 200000

ans_file = open("avito_result.json", "w")
ans_file.write("[")

for filter_cost in range(13500000, 60000000, step):
    params = {
        "categoryId": 24,
        "locationId": 637640,
        "pmin": 0,
        "pmax": 0,
        "cd": 0,
        "params[201]": 1059,
        "params[499][]": 5255,
        "params[110472][]": 437129,
        "verticalCategoryId": 1,
        "rootCategoryId": 4,
        "localPriority": 0,
        "proprofile": 1,
        "useReload": "true"
    }
    url = "https://www.avito.ru/js/catalog"
    params["pmin"] = filter_cost
    params["pmax"] = filter_cost + step - 1

    try:
        sleep(3)
        r = scraper.get(url, params=params)
        url = "https://www.avito.ru" + r.json()["url"]
    except Exception as e:
        print("error in script", e)
        continue

    for p in range(1, 10): # return big number
        sleep(3)
        # try:
        r = scraper.get(url, params={"p": p})
        soup = BeautifulSoup(r.text, "html.parser")
        # r = driver.get(url)
        # soup = BeautifulSoup(driver.page_source, "html.parser")

        print("page:", p)

        with open("avito.html", "w") as f:
            f.write(r.text)

        links = ["https://www.avito.ru" + i.get("href") for i in soup.find_all("a", "iva-item-sliderLink-uLz1v")]
        # links = ["https://www.avito.ru/moskva/kvartiry/kvartira-studiya_27m_226et._2848783711"]
        # print(links)

        all_params = set({'Id', 'Url', 'Цена', 'Метро', 'Этажей в доме', 'Ремонт', 'Санузел', 'Высота потолков', 'Грузовой лифт', 'Жилая площадь', 'Вид сделки', 'Техника', 'Отделка', 'Способ продажи', 'Тип комнат', 'Тип участия', 'Этаж', 'Корпус, строение', 'Балкон или лоджия', 'Пассажирский лифт', 'Название новостройки', 'Окна', 'Общая площадь', 'Двор', 'В доме', 'Площадь кухни', 'Количество комнат', 'Официальный застройщик', 'Тип дома', 'Парковка', 'Год постройки', 'Срок сдачи', 'Просмотры', 'Дата выхода', 'Дата парсинга'})
        all_params_buf = ['Id', 'Url', 'Цена', 'Метро', 'Этажей в доме', 'Ремонт', 'Санузел', 'Высота потолков', 'Грузовой лифт', 'Жилая площадь', 'Вид сделки', 'Техника', 'Отделка', 'Способ продажи', 'Тип комнат', 'Тип участия', 'Этаж', 'Корпус, строение', 'Балкон или лоджия', 'Пассажирский лифт', 'Название новостройки', 'Окна', 'Общая площадь', 'Двор', 'В доме', 'Площадь кухни', 'Количество комнат', 'Официальный застройщик', 'Тип дома', 'Парковка', 'Год постройки', 'Срок сдачи', 'Просмотры', 'Дата выхода', 'Дата парсинга']

        if len(links) == 0:
            break
        end = False
        
        for link in links:
            try:
                if not 'moskva' in link:
                    end = True
                    break
                print("cost: " + str(filter_cost) + ", url: " + link)
                sleep(3)
                # driver.get(link)
                # soup = BeautifulSoup(driver.page_source, "html.parser")
                # print("go")
                r = scraper.get(link)
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
                    all_params.add(key)
                    if key in all_params:
                        cur_params[key] = value
                
                params = soup.find_all("li", class_="style-item-params-list-item-aXXql")
                for i in params:
                    key, value = unicodedata.normalize("NFKD", i.text).split(':')
                    value = value[1:]
                    all_params.add(key)
                    if key in all_params:
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
                        d = datetime.datetime.combine(d, datetime.datetime.min.time())
                    # print(date, d)
                    unixtime = time.mktime(d.timetuple())
                    cur_params["Дата выхода (unixtime)"] = unixtime
                    cur_params["Разница в днях"] = (datetime.datetime.now() - d).days
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


                ans_file.write(json.dumps(cur_params)) 
                ans_file.write(",")
                # result.append(cur_params)
                # csv_writer.csv_add_rows("avito_test.csv", [cur_params], all_params, first)
                first = False

                # print(cur_params)
            except Exception as e:
                problem_links.append(link)
                print("excetion durind link:", e, link)
        if end:
            break
        # except Exception as e:
        #     print("aboba(", e)
ans_file.write(']')

print("Problem links:", problem_links)
print("Total problem links:", len(problem_links))
# with open("avito_result.json", 'w') as f:
    # f.write(json.dumps(result))

# https://www.avito.ru/js/catalog?_=&categoryId=24&locationId=637640&pmin=2000000&pmax=6003400&cd=0&params[201]=1059&params[499][]=5255&params[110472][]=437129&verticalCategoryId=1&rootCategoryId=4&localPriority=0&proprofile=1&useReload=true

