from abc import ABCMeta, abstractmethod

class Scrapper(metaclass=ABCMeta):
    def __init__(self):
        self.features = {}

    @abstractmethod
    def get_links(self):
        pass

    @abstractmethod
    def scrap_link(self, link):
        pass