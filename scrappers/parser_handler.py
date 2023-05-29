from scrappers.scrapper import Scrapper
from utils.csv_writer import csv_add_rows
import random
import json
from itertools import product
import time

import sys

class Handler:
    def __init__(self) -> None:
        pass

    def GenerareFilter(self, settings):
        filters = []
        if settings["get_iterate"] == {}:
            filters.append({})
        else:
            keys = list(settings["get_iterate"].keys())
            keys.remove("type")
            values = []
            for key in keys:
                values.append(eval(settings["get_iterate"][key]))

            if settings["get_iterate"]["type"] == "linear":
                mult_values = zip(*values)
                # settings = {'a': [1, 2], 'b': [3, 4]} -> 
                # keys = {'a', 'b'}
                # mult_values = [[1, 3], [2, 4]]
            else:
                mult_values = product(*values)
                # settings = {'a': [1, 2], 'b': [3, 4, 5]} -> 
                # keys = {'a', 'b'}
                # mult_values = [[1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]

            for value in mult_values:
                filters.append(dict(zip(keys, value)))

            # linear -> [{a : 1, b : 3}, {a : 2, b : 4}]
            # pairwise -> filters = [{a : 1, b : 3}, {a : 1, b : 4}, ..., {a : 2, b : 5}]
        return filters

    def Do(self, scrappers, all_settings):
        for parser in scrappers:
            settings = all_settings["parsers"][parser.name]

            all_links = []

            # надо перебрать возможные варианты параметров фильтрации
            filters = self.GenerareFilter(settings)
            # print("filters:", filters)

            for filter in filters:
                try:
                    params = filter | settings["get_other_params"]
                    print("params =", params)
                    new_links = parser.get_links(params=params)
                except Exception as e:
                #     # add logging
                     print("[ERROR] Exception occured with parser " + parser.name)
                     print(e)
                     new_links = []

                all_links += new_links

            # тут мы уже собрали все ссылочки и собираемся из них доставать инфу
            # пока что в этой части не знаю что можно конфигурировать кроме названия файла
            print(all_links)
            print("go write to file")
            parser.features = settings["features"]
            # print(json.dumps(list(settings["features"].keys()))[0])

            first = True
            cnt = 0
            for link in all_links:
                if random.random() > 0.99:
                    print(cnt, len(all_links))
                data = None

                try: 
                    data = parser.scrap_link(link)
                except Exception as e:
                    print(e)
                    data = None
                    print("[ERROR] when parsing data with " + parser.name)

                if data:
                    csv_add_rows(settings["filename"], [data], list(settings["features"].keys()), first)
                    first = False
                else:
                    print("[WARNING] Data is None")
                cnt += 1

            print("[INFO] end of parser " + parser.name)
