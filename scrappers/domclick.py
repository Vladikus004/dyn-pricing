import scrappers.scrapper as scrapper
from utils.api.domclick import __DomclickApi as API

class Domclick(scrapper.Scrapper):
    def __init__(self) -> None:
        self.name = "domclick"

    def get_links(self, params={}):
        search_layouts_json = API.search(params)
        links = []

        for item_num in range(len(search_layouts_json["search"]["itemsClean"])):
            flat_data = { # по идее надо учиться доставать это из ссылки, а не так делать
                "aids": params["aids"]
            }
            flat_id = search_layouts_json["search"]["itemsClean"][item_num]["id"]
            flat_data["id"] = flat_id # то же самое что и с aids
            links.append(flat_data)

        return links
    
    def scrap_link(self, flat_data):
        id = flat_data["id"]
        aids = flat_data["aids"]

        data = API.get_new_flat(id)

        offer = data["result"]
        ans = {}

        # id 
        ans['id'] = offer["id"]

        # main info
        ans['offer_type'] = offer.get("offer_type")
        ans['aids'] = aids


        # price info
        ans['obj_price'] = offer["price_info"].get("price")
        ans['obj_sq_price'] = offer["price_info"].get("square_price")

        price_history = []
        if "price_history" in offer["price_info"]:
            for hst in offer["price_info"]["price_history"]:
                price_history.append((hst["date"], hst["price"]))
        ans['price_history'] = price_history

        if ("building" in offer):
            # building info 
            ans['building_start_build_year'] = offer["building"].get("start_build_year")
            ans['building_end_build_year'] = offer["building"].get("end_build_year")
            ans["building_wall_type"] = offer["building"].get("wall_type", {'display_name':None})["display_name"]
            ans["building_kind"] = offer["building"].get("kind", {'display_name':None})["display_name"]
            ans["building_readiness_percentage"] = offer["building"].get("readiness_percentage")
            ans["building_floors"] = offer["building"].get("floors")
        else:
            print("no building in {}".format(id))

        # obj info
        ans['obj_area'] = offer["object_info"].get("area")
        ans['obj_balconies'] = offer["object_info"].get("balconies")
        ans['obj_living_area'] = offer["object_info"].get("living_area")
        ans['obj_kitchen_area'] = offer["object_info"].get("kitchen_area")
        ans['obj_rooms'] = offer["object_info"].get("rooms")
        ans['obj_floor'] = offer["object_info"].get("floor")
        ans['obj_renovation'] = offer["object_info"].get("renovation", {'display_name':None})["display_name"]

        obj_window_view = []
        if offer["object_info"].get("window_view"):
            for view in offer["object_info"].get("window_view"):
                obj_window_view.append(view["display_name"])
        ans['obj_window_view'] = obj_window_view

        # offer info                             default = {0, 0}
        ans['calls_count'] = offer.get("offer_stat", {'calls_count' : 0}).get("calls_count")
        ans['views_count'] = offer.get("offer_stat", {'views_count' : 0}).get("views_count")

        # address
        ans['address_name'] = offer["address"].get("display_name")
        
        address_subways = []
        if offer["address"].get("subways"):
            for subway in offer["address"].get("subways"):
                address_subways.append((subway["display_name"],
                                        subway["distance"],
                                        subway["time_on_foot"],
                                        subway["meta"]["line_name"]))
        ans['address_subways'] = address_subways

        # published date
        ans['published'] = offer.get('published_dt')
        ans['published_formated'] = ans['published'][:10]

        return ans
