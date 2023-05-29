from datetime import datetime
from bs4 import BeautifulSoup
import requests 
import csv


if __name__=='__main__':
    url = 'https://www.cbr.ru/hd_base/KeyRate/?UniDbQuery.Posted=True&UniDbQuery.From=17.09.2013&UniDbQuery.To='
    today = datetime.today().strftime('%d.%m.%Y')
    url += today

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    data = soup.find(class_="data")
    objects = data.find_all("tr")
    objects.pop(0)
    objects = reversed(objects)

    file = open('keyratedata.csv', 'w', encoding="UTF8")
    writer = csv.writer(file)

    for obj in objects:
        date_data = obj.find_all("td")
        writer.writerow([date_data[0].text, float(date_data[1].text.replace(',', '.'))])

    file.close()