from typing import List


class Category:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

class Categories:
    def __init__(self, category_list: List[Category]):
        self.category_list = category_list
    def __getitem__(self, index):
        return self.category_list[index]