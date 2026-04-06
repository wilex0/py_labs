from sys import path
path.append("/home/wilex/Документы/GitHub/py_labs")

from src.lab01.model import Product
from src.lab01.validate import *


class ProductCollection:
    __DEFAULT_CAP = 10

    @property
    def size(self):
        return self.__curr_pos + 1

    def __init__(self, capacity:int):
        if not capacity:
            capacity = ProductCollection.__DEFAULT_CAP
        validate_vals(capacity)
        self.__items = [None] * capacity
        self.__curr_pos = 0
    def append(self, p:Product):
        self.__validate_product(p)
        self.__items[self.__curr_pos] = p  
        self.__curr_pos += 1
    def __iter__(self):
        return iter(self.__items)
    def remove(self, p:Product):
        self.__validate_product(p)
        for i,v in enumerate(self.__items):
            self.__validate_product(v)
            if v.id == p.id:
                self.__items.pop(i)
    def get_all(self):
        return self.__items
    
    def find_by_cost(self, min:int, max:int):
        validate_vals(min); validate_vals(max)
        res = []
        for i in self.__items:
            if min <= i.curr_cost <= max:
                res.append(i)
        if not len(res):
            return None
        return res

    def find_by_quantity(self, min:int, max:int):
        validate_vals(min); validate_vals(max)
        res = []
        for i in self.__items:
            if min <= i.quantity <= max:
                res.append(i)
        if not len(res):
            return None
        return res
    
    def find_by_name(self, name:str):
        validate_strs(name)
        res = []
        for i in self.__items:
            if i.name == name:
                res.append(i)
        if not len(res):
            return None
        return res
    
    def find_by_size(self, size:Size):
        validate_size(size)
        res = []
        for i in self.__items:
            if i.size == size:
                res.append(i)
        if not len(res):
            return None
        return res
    
    def __len__(self):
        return self.__curr_pos + 1

    def __validate_product(self, p):
        if not isinstance(p, Product):
            raise TypeError("Incorrect object type")