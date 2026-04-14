from sys import path

from models import *


class ProductCollection:
    def __init__(self, arr=None):
        if arr:
            for i in arr:
                self.__validate_product(i)
            self.__items = arr
        else:
            self.__items = []
    def append(self, p:Product):
        self.__validate_product(p)
        if (self.find_by_name(p.name) and self.find_by_seller(p.seller)) or self.find_by_id(p.id):
            raise ValueError("Can't add same product")
        self.__items.append(p)
    def __iter__(self):
        return iter(self.__items)
    def __len__(self):
        return len(self.__items)
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
        res = [i for i in self.__items if min <= i.curr_cost <= max]
        if not len(res):
            return None
        return ProductCollection(res)

    def find_by_quantity(self, min:int, max:int):
        validate_vals(min); validate_vals(max)
        res = [i for i in self.__items if min <= i.quantity <= max]
        if not len(res):
            return None
        return ProductCollection(res)
    
    def find_by_name(self, name:str):
        validate_strs(name)
        res = [i for i in self.__items if i.name.lower() == name.lower()]
        if not len(res):
            return None
        return ProductCollection(res)
    
    def find_by_size(self, size:Size):
        validate_size(size)
        res = [i for i in self.__items if i.size == size]
        if not len(res):
            return None
        return ProductCollection(res)
    
    def find_by_seller(self, seller:str):
        validate_strs(seller)
        res = [i for i in self.__items if i.seller == seller]
        if not len(res):
            return None
        return ProductCollection(res)

    def find_by_id(self, id:int):
        for i in self.__items:
            if i.id == id:
                return i
        return None

    def sort_by_name(self, reverse=False):
        self.__items.sort(key=lambda x: x.name, reverse=reverse)
    def sort_by_quantity(self, reverse=False):
        self.__items.sort(key=lambda x: x.quantity, reverse=reverse)
    def sort_by_cost(self, reverse=False):
        self.__items.sort(key=lambda x: x.cost, reverse=reverse)
    def sort_by_id(self, reverse=False):
        self.__items.sort(key=lambda x: x.id, reverse=reverse)
    def sort_by_size(self, reverse=False):
        self.__items.sort(key=lambda x: x.size, reverse=reverse)

    def filter(self, pred):
        n_list = ProductCollection()
        for i in self.__items:
            if pred(i):
                n_list.append(i)
        return n_list
    
    def __str__(self):
        res = ""
        for i, v in enumerate(self.__items):
            res += f"{i + 1}. " + str(v) + '\n'
        return res

    def __validate_product(self, p):
        if not isinstance(p, Product):
            raise TypeError("Incorrect object type")
    
    def get_has_quantity(self):
        return self.filter(lambda x: x.quantity)
    def get_less_than(self, cost:int):
        validate_vals(cost)
        return self.filter(lambda x: x.curr_cost < cost)