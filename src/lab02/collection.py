from sys import path
path.append("/home/wilex/Документы/GitHub/py_labs")

from src.lab01.model import Product
from src.lab01.validate import *


class ProductCollection:
    __DEFAULT_CAP = 10
    
    @property
    def size(self):
        return self.__curr_pos + 1

    def __init__(self):
        self.__items = []
    def append(self, p:Product):
        self.__validate_product(p)
        self.__items.append(p)
    def __iter__(self):
        return iter(self.__items)
    def remove(self, p:Product):
        self.__validate_product(p)
        for i,v in enumerate(self.__items):
            self.__validate_product(v)
            if v.id == p.id:
                self.__items.pop(i)
    def __getitem__(self, i:int):
        validate_vals(i)
        if i < 0:
             i += len(self.__items)
        if i < 0 or i >= len(self.__items):
            raise IndexError("Index out of range")
        return self.__items[i]

    def remove_at(self, i:int):
        validate_vals(i)
        del self.__items[i]
    
    def get_all(self):
        return self.__items.copy()
    
    def find_by_cost(self, min:int, max:int):
        validate_vals(min); validate_vals(max)
        res = [i for i in self.__items if min <= i <= max]
        if not len(res):
            return None
        return res

    def find_by_quantity(self, min:int, max:int):
        validate_vals(min); validate_vals(max)
        res = [i for i in self.__items if min <= i.quantity <= max]
        if not len(res):
            raise ValueError(f"Product with {min} to {max} doesn't find")
        return res
    
    def find_by_name(self, name:str):
        validate_strs(name)
        res = [i for i in self.__items if i.name.lower() == name.lower()]
        if not len(res):
            raise ValueError(f"Product with {name} name doesn't find")
        return res
    
    def find_by_size(self, size:Size):
        validate_size(size)
        res = [i for i in self.__items if i == size]
        if not len(res):
            raise ValueError(f"Product with {size} size doesn't find")
        return res
    
    def __len__(self):
        return self.__curr_pos + 1

    def __validate_product(self, p):
        if not isinstance(p, Product):
            raise TypeError("Incorrect object type")