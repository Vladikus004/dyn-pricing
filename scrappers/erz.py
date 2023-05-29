import scrappers.scrapper as scrapper
import utils.find
import requests
import json

headers = {
    "accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52"
}

class Erz(scrapper.Scrapper):
    def __init__(self) -> None:
        self.name = "erz"

    def get_links(self, params):
        list_id = []
        url = 'https://erzrf.ru/erz-rest/api/v1/gk/table' # перенести в API
        req = requests.get(url, params=params, headers=headers)
    
        # print(req.text)

        data = json.loads(req.text)
        for i in range(10):
            list_id.append(data["list"][i]["gkId"])
        return list_id

        


    def scrap_link(self, res_link):
        url = 'https://erzrf.ru/erz-rest/api/v1/gk/list-map/?gkId='+ res_link + '&region=moskva&regionKey=143443001&costType=1&sortType=qrooms'
        req = requests.get(url, headers=headers)
        src = req.text
        data = json.loads(src)

        ans = {}
        # print(self.features.keys())
        # exit(0)
        for feature, path in self.features.items():
            ans[feature] = utils.find.find(path, data)           

        # не будем конфигурировать
        url = 'https://erzrf.ru/erz-rest/api/v1/gk/advantages/'+ res_link
        req = requests.get(url, headers=headers)

        src = req.text
        data = json.loads(src)

        another_data = {}

        for n in range(len(data)):
            for m in range(len(data[n]['values'])):
                another_data[str(data[n]['values'][m]['name'])] = data[n]['values'][m]['mark']
            
        ans["another_data"] = another_data

        # ans['sales_info'] = {}
        # if req.ok:
        #     src = req.text
        #     data = json.loads(src)
        #     for n in range(len(data['data']['salesGraphDtos'])):
        #         ans['sales_info'][n] = {}
        #         ans['sales_info'][n]['reportMonthDt'] = data['data']['salesGraphDtos'][n]['reportMonthDt']
        #         ans['sales_info'][n]['realised'] = data['data']['salesGraphDtos'][n]['realised']
        #         ans['sales_info'][n]['contracted'] = data['data']['salesGraphDtos'][n]['contracted']
        #         ans['sales_info'][n]['areaSq'] = data['data']['salesGraphDtos'][n]['areaSq']
        #         ans['sales_info'][n]['priceAvg'] = data['data']['salesGraphDtos'][n]['priceAvg']
        return ans
