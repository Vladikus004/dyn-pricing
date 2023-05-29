import scrappers.scrapper as scrapper
import utils.find
import requests
import json

headers = {
    "accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52"
}

class NashDom(scrapper.Scrapper):
    def __init__(self) -> None:
        self.name = "nashdom"

    def get_links(self, params):
        res_links = []
        url = 'https://наш.дом.рф/сервисы/api/kn/object/map' # перенести в API
        req = requests.get(url, params=params)
        data = json.loads(req.text)

        for layout in data['data']['list']:
            res_links.append(layout['objId'])

        return res_links


    def scrap_link(self, res_link):
        url1 = 'https://наш.дом.рф/сервисы/api/object/'
        url2 = url1 + str(res_link)
        req = requests.get(url2, headers=headers)
        src = req.text
        data = json.loads(src)

        ans = {}
        # print(self.features.keys())
        # exit(0)
        for feature, path in self.features.items():
            ans[feature] = utils.find.find(path, data)           

        # не будем конфигурировать
        url3 = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/сервисы/api/object/' + str(res_link) + '/sale_graph?type=apartments'
        req = requests.get(url3, headers=headers)
        ans['sales_info'] = {}
        if req.ok: 
            src = req.text
            data = json.loads(src)
            for n in range(len(data['data']['salesGraphDtos'])):
                ans['sales_info'][n] = {}
                ans['sales_info'][n]['reportMonthDt'] = data['data']['salesGraphDtos'][n]['reportMonthDt']
                ans['sales_info'][n]['realised'] = data['data']['salesGraphDtos'][n]['realised']
                ans['sales_info'][n]['contracted'] = data['data']['salesGraphDtos'][n]['contracted']
                ans['sales_info'][n]['areaSq'] = data['data']['salesGraphDtos'][n]['areaSq']
                ans['sales_info'][n]['priceAvg'] = data['data']['salesGraphDtos'][n]['priceAvg']
        return ans
