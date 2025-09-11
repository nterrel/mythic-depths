import pygame


class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.name] = self.items.get(item.name, 0) + 1
