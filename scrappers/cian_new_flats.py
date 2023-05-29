import scrappers.scrapper as scrapper
import cloudscraper
import json
import sys
import re
import utils.find

class CianNewFlats(scrapper.Scrapper):
    def __init__(self) -> None:
        self.name = "cian_new_flats"
        self.scrapper = cloudscraper.create_scraper(
            # browser={
            #     'browser': 'firefox',
            #     'platform': 'windows',
            #     'mobile': False
            # },
            # interpreter='nodejs', 
            # captcha={'provider': 'return_response'} 
            debug=True
        )

    def get_links(self, params={}):
        res_links = []
        page_data = {
            "p" : 1
        }
        page = 1
        while True: 
            page_data["p"] = page
            # url = "https://www.cian.ru/cat.php"
            url = 'https://www.cian.ru/kupit-kvartiru-novostroyki/'
            r = self.scrapper.get(url=url, params=params | page_data)
            print(re.split('&|\?', r.url))
            if "p=1" in re.split('&|\?', r.url) and page != 1:
                break 
            char1 = "window._cianConfig['frontend-serp'] = (window._cianConfig['frontend-serp'] || []).concat("
            char2 = '</'

            with open("text.txt", "w") as file:
                file.write(r.text)

            text = r.text
            start_pos = text.find(char1) + (len(char1))
            res = text[start_pos:text.find(char2, start_pos) - len(char2)]
            
            with open("res.txt", "w") as file:
                file.write(res)

            data = json.loads(res)

            offers = data[94]["value"]["results"]["offers"]

            was_append = False
            for offer in offers:
                res_links.append(offer["id"])
                was_append = True
            
            page += 1
            if not was_append:
                break

        return res_links


    def scrap_link(self, res_link):
        url = "https://www.cian.ru/sale/flat/" + str(res_link)
        r = self.scrapper.get(url=url)
        text = r.text

        char1 = "window._cianConfig['frontend-offer-card'] = (window._cianConfig['frontend-offer-card'] || []).concat("
        char2 = '</'

        start_pos = text.find(char1) + (len(char1))
        res = text[start_pos: text.find(char2, start_pos) - 3]

        try:
            data = json.loads(res)
        except Exception as e:
            print("Can't parse json, url = " + url)
            return None
        ans = {}

        with open("data.json", "w") as file:
            file.write(json.dumps(data))

        for feature, path in self.features.items():
            ans[feature] = utils.find.find(path, data)
            if type(ans[feature]) == str:
                ans[feature] = ans[feature].replace(';', ',')

        flat_data = data[117]["value"]
        offer_data = flat_data["offerData"]
        offer = flat_data["offerData"]["offer"]



        ans["address"] = []
        for i in offer["geo"]["address"]:
            in_map = {
                "fullName": i["fullName"],
                "type": i["type"]
            }
            ans["address"].append(in_map)

        ans["priceChanges"] = []
        for i in offer_data["priceChanges"]:
            in_map = {
                "changeTime": i["changeTime"].replace(';', ','),
                "priceDataCurrency": i["priceData"]["currency"],
                "priceDataPrice": i["priceData"]["price"]
            }
            ans["priceChanges"].append(in_map)
        
        with open("data.json", "w") as file:
            file.write(json.dumps(flat_data))
        
        return ans