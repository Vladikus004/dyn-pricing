from scrappers.domclick import Domclick
from scrappers.nashdom import NashDom
from scrappers.erz import Erz
from scrappers.cian_layouts import CianLayouts
from scrappers.parser_handler import Handler
from scrappers.cian_new_flats import CianNewFlats
from scrappers.avito import Avito

import json
from loguru import logger

if __name__=='__main__':
    parser_handler = Handler()

    registered_parsers = [Avito()]
    with open('config.json', 'r') as file:
        json_data = file.read()

    parser_handler.Do(registered_parsers, json.loads(json_data))
