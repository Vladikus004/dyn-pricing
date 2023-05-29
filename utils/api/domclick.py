import requests
import json

class DomclickApi:
    def __init__(self): 
        self.host = 'https://domclick.ru/'
        self.internal_api_offer_list = 'https://offers-service.domclick.ru/research/v3/offers'
        self.search_url = "https://domclick.ru/search"
        self.internal_api_new_flat = "https://offer-card.domclick.ru/api/v3/offers/sale/new_flats/"

        # это стоит переписать к примеру на 
        # открытие странички в селениуме и выгрузкой этих cookie 
        self.cookies = {'qrator_ssid':'1677432077.489.yQ4V9VpKTLByMSq5-u684a9ruga7agvifovoh9hhj3i6tibi8', 
                        'qrator_jsid':'1677432086.572.HPZHZngXs66zQdZ7-62dtfsrrkc6q7k77tlrkg709p14jergn'}
        self.session = requests.Session()
        self.retries = 2 # забирать из конфига

    def find_json(self, text):
        json_pattern = "window.__data={"
        start_json_index = text.find(json_pattern)
        end_json_index = text.find(";</script>", start_json_index)
        return (start_json_index + len(json_pattern) - 1, end_json_index)


    def get(self, url, params={}): 
        answer = self.session.get(url=url, cookies=self.cookies, params=params)
        retry = 1 
        while not answer.ok and retry <= self.retries:
            answer = self.session.get(url=url, cookies=self.cookies, params=params)
            retry += 1
        
        if not answer.ok: 
            print("[API ERROR] answer.ok = False, url="+answer.url)
            # add normal logging
            # throw 

        return answer

    def search(self, params={}):
        answer = self.get(self.search_url, params)
        start_json_index, end_json_index = self.find_json(answer.text)
        return json.loads(answer.text[start_json_index:end_json_index])

    def get_new_flat(self, flat_id):
        answer = self.get(self.internal_api_new_flat + str(flat_id))
        return answer.json()

__DomclickApi = DomclickApi()

#TODO: add normal exception handlers
#TODO: add logging
