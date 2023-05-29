import cloudscraper
import json

class Cloudflare():
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'firefox',
                'platform': 'windows',
                'mobile': False
            }
        )

    def get(self, url, params):
        return self.scrapper.get(url=url, params=params)

    def cian_get_list(self, url, params):
        r = self.get(url, params)
        char1 = "window._cianConfig['newbuilding-search-frontend'] = (window._cianConfig['newbuilding-search-frontend'] || []).concat("
        char2 = '</'

        text = r.text
        start_pos = text.find(char1) + (len(char1))
        res = text[start_pos: text.find(char2, start_pos) - 3]

        data = json.loads(res)

    def avito_get_hashed_url(self, params):
        r = self.scraper.get("https://www.avito.ru/js/catalog", params=params)
        url = "https://www.avito.ru" + r.json()["url"]
        return url

__Cloudflare = Cloudflare()