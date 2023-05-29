import scrappers.scrapper as scrapper
import cloudscraper
import json
import sys
import utils.find

class CianLayouts(scrapper.Scrapper):
    def __init__(self) -> None:
        self.name = "cian_layouts"
        self.scrapper = cloudscraper.create_scraper(
            browser={
                'browser': 'firefox',
                'platform': 'windows',
                'mobile': False
            }
        )

    def get_links(self, params={}):
        res_links = []

        url = 'https://www.cian.ru/newobjects/list/'
        r = self.scrapper.get(url=url, params=params)
        print(r.url)
        char1 = "window._cianConfig['newbuilding-search-frontend'] = (window._cianConfig['newbuilding-search-frontend'] || []).concat("
        char2 = '</'

        text = r.text
        start_pos = text.find(char1) + (len(char1))
        res = text[start_pos: text.find(char2, start_pos) - 3]

        # with open("rtext", "w") as file:
        #     file.write(text)

        # with open("data.json", "w") as file:
        #     file.write(json.dumps(data))

        data = json.loads(res)

        for i in range(len(data[18]['value']['offersData']['newbuildings'])):
            res_links.append(data[18]['value']['offersData']['newbuildings'][i]['url'])

        return res_links


    def scrap_link(self, res_link):
        url = res_link
        r = self.scrapper.get(url=url)
        text = r.text

        char1 = "window._cianConfig['newbuilding-card-desktop-fichering-frontend'] = (window._cianConfig['newbuilding-card-desktop-fichering-frontend'] || []).concat("
        if text.find(char1) == -1:
            char1 = "window._cianConfig['newbuilding-card-desktop-frontend'] = (window._cianConfig['newbuilding-card-desktop-frontend'] || []).concat("
        char2 = '</'
        
        start_pos = text.find(char1) + (len(char1))
        res = text[start_pos: text.find(char2, start_pos) - 3]

        with open("rtext", "w") as file:
            file.write(text)
        try:
            data = json.loads(res)
        except Exception as e:
            with open("aboba.txt", "w") as file:
                file.write(text)
            print("Can't parse json, url = " + url)
            return None
        ans = {}

        # with open("data.json", "w") as file:
            # file.write(json.dumps(data))
        # print(type(data))

        for feature, path in self.features.items():
            ans[feature] = utils.find.find(path, data)
            if type(ans[feature]) == str:
                ans[feature] = ans[feature].replace(';', ',')


        avg_layout_data = data[28]['value']['newbuilding']['specifications']
        for layout_data in avg_layout_data:
            try:
                ans[layout_data['itemType']] = layout_data['value']
            except Exception:
                print(layout_data['itemType'] + " not found in json")
                ans[layout_data['itemType']] = None
        # ans['id'] = data[28]['value']['newbuilding']['id']
        # ans['name'] = data[26]['value']['newbuilding']['name']
        # ans['infrastructureFromBuilder_rate'] = data[26]['value']['newbuilding']['transportAccessibilityRate']['infrastructureFromBuilder']['rate']
        # ans['transportAccessibility_rate'] = data[26]['value']['newbuilding']['transportAccessibilityRate']['transportAccessibility']['rate']
        # ans['newbuildingClassName'] = data[26]['value']['newbuilding']['newbuildingClassName']
        # ans['ceilingHeight'] = data[26]['value']['newbuilding']['ceilingHeight']
        # ans['floor'] = data[26]['value']['newbuilding']['floor']

        # ans['materials'] = []
        # for i in data[26]['value']['newbuilding']['materials']:
        #     ans['materials'].append(i)

        # ans['interiorDecoration'] = []
        # for i in data[26]['value']['newbuilding']['interiorDecoration']:
        #     ans['interiorDecoration'].append(data[26]['value']['newbuilding']['interiorDecoration'][i]['title'])

        # ans['infrastructure'] = []
        # for i in data[26]['value']['newbuilding']['infrastructure']:
        #     ans['infrastructure'].append(data[26]['value']['newbuilding']['infrastructure'][i]['name'])

        # ans['isReliable'] = data[26]['value']['newbuilding']['isReliable']
        # ans['hasProblems'] = data[26]['value']['newbuilding']['hasProblems']
        # ans['isEscrow'] = data[26]['value']['newbuilding']['isEscrow']

        # ans['problems'] = []
        # for i in data[26]['value']['newbuilding']['problems']:
        #     ans['problems'].append(i)

        # ans['isSalesLeader'] = data[26]['value']['newbuilding']['isSalesLeader']
        # ans['isUpcomingSale'] = data[26]['value']['newbuilding']['isUpcomingSale']
        return ans