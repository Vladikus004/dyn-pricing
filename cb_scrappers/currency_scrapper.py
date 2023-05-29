import datetime
import requests
from bs4 import BeautifulSoup
import csv

if __name__=="__main__":
    url = "https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To="
    
    try:
        scrap_file = open('data/last_scrap', 'r')
    except Exception as e: 
        scrap_file = open('data/last_scrap', 'w')
        scrap_file.write('20.11.2013')
        scrap_file.close()
        scrap_file = open('data/last_scrap', 'r')

    from_date = scrap_file.read() 
    print(from_date)

    date_array = from_date.split('.')
    date_array = [int(i) for i in date_array]

    from_date = datetime.datetime(date_array[2], date_array[1], date_array[0])
    delta = datetime.timedelta(1)

    to_date = datetime.datetime.today()

    file = open('data/currency_data.csv', 'a', encoding="UTF8")
    writer = csv.writer(file)

    try:
        while from_date < to_date:
            current_date = from_date.strftime('%d.%m.%Y')
            current_url = url + current_date

            req = requests.get(current_url)
            
            if req.status_code != 200:
                print ("error parsing " + url)
                continue

            soup = BeautifulSoup(req.text, 'html.parser')

            real_date = soup.find(class_='datepicker-filter_button')
            real_date = real_date.text

            print (current_date)

            data = soup.find(class_="data")
            objects = data.find_all("tr")
            objects.pop(0)
            for obj in objects: 
                row = obj.find_all("td")
                write_data = [current_date, real_date]
                if row[1].text in ["USD", "EUR"]:
                    for i in row:
                        write_data.append(i.text.replace(',', '.'))

                    # print (write_data)
                    writer.writerow(write_data)

            from_date += delta
    except BaseException:
        pass

    file.close()
    scrap_file.close()

    scrap_file = open('data/last_scrap', 'w')
    scrap_file.write(from_date.strftime('%d.%m.%Y'))
    # print(from_date.strftime('%d.%m.%Y'))