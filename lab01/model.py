from enum import Enum
from re import sub
from datetime import date, datetime, time
from colorama import Fore, Style
from validate import *
from enums import *

from os import *

import sys

from json import dumps, loads

class Product:
    __MAX_N_HISTORY = 10
    __Id = 0

    @property
    def size(self):
        return self.__size
    
    @size.setter
    def size(self, new_size:Size):
        validate_size(new_size)
        self.__size = new_size
    
    @property
    def name(self):
        return self.__name 
    
    @name.setter
    def name(self, new_name:str):
        validate_strs(new_name)
        self.__name = sub(r'( )+', ' ', new_name.strip())
    
    @property
    def seller(self):
        return self.__seller
    
    @seller.setter
    def seller(self, new_seller:str):
        validate_strs(new_seller)
        self.__seller = new_seller

    @property 
    def cost(self):
        return self.__cost
    
    @property
    def curr_cost(self):
        if self.discount:
            return self.__cost * (1 - self.discount / 100)
        return self.__cost
        
    @property
    def description(self):
        return self.__desc

    @description.setter
    def description(self, new_desc):
        validate_strs(new_desc)
        self.__desc = new_desc
    
    @property
    def discount(self):
        if (all(v is None for v in self.__histoty)):
            return 0
        return self.__top_item[1]
    
    @property
    def id(self):
        return self.__id
    
    @property
    def history(self):
        return [ i for i in self.__histoty if i != None]

    @property
    def top_item(self):
        if self.__top_item != None:
            return self.__top_item
    #constructors
    def __init__(self, cost:int, name:str, seller:str, description:str, size:Size):
        self.size = size
        self.name = name
        self.description = description
        self.seller = seller

        validate_vals(cost)
        self.__cost = cost

        self.__cur_ptr = 0
        self.__histoty = Product.__MAX_N_HISTORY * [None]
        self.__top_item = None

        self.__id = Product.__Id + 1
        Product.__Id += 1

    @classmethod
    def load_from_json(cls, json:str):
        res = loads(json)
        prod = cls(int(res["cost"]), res["name"], res["seller"], res["description"], Size(res["size"]))
        prod.__id = res["id"]
        Product.__Id -= 1
        
        if "discount" in res.keys():
            prod.push_discount(int(res["discount"]), datetime.strptime(res["last_disctount_time"], "%Y-%m-%d"))
        return prod

    #private method
    def __prefix_ptr(self, op):
        if not op in ('+', '-'):
            return None
        if op == '+':
            self.__cur_ptr = self.__cur_ptr + 1 if self.__cur_ptr != Product.__MAX_N_HISTORY - 1 else 0
        else:
            self.__cur_ptr = self.__cur_ptr - 1 if self.__cur_ptr != 0 else Product.__MAX_N_HISTORY - 1

        return self.__cur_ptr

    #discount methods
    def push_discount(self, percent, time:datetime=datetime.now()):
        validate_percent(percent)
        validate_date(time)

        if self.__top_item is None or self.__top_item[2] < time:
            self.__histoty[self.__cur_ptr] = (self.__cost * (1 - percent / 100), percent, time)
            self.__top_item = self.__histoty[self.__cur_ptr]
            self.__prefix_ptr('+')
        else:
            raise RuntimeError("Can't use this item")

    def pop_discount(self):
        self.__prefix_ptr('-')
        self.__top_item = self.__histoty[self.__cur_ptr - 1]

    def clear_duscount(self):
        for i in range(Product.__MAX_N_HISTORY):
            self.__histoty[i] = None
        self.__cur_ptr = 0
        self.__top_item = None

    #output method
    def write_data(self, style:Style=Style.NORMAL, color: Fore=Fore.WHITE, width=50, height = 20, fd:int=sys.stdout.fileno()):
        if fd != sys.stdout.fileno():
            res = None
            if self.__histoty[self.__cur_ptr - 1] is None:
                res = { "name":self.__name, "id": self.__id, "description":self.__desc, "seller": self.__seller, "cost": self.__cost, "size": self.__size.value }
            else:
                res = { "name":self.__name, "id": self.__id, "description":self.__desc, "seller": self.__seller, "cost": self.__cost, "size": self.__size.value, "discount":self.__top_item[1], "last_disctount_time": str(self.__top_item[2].date()) }
            write(fd, dumps(res).encode())
        else:
            if len(self.name) > width - 2:
                width = len(self.name) + 20
            res = ''
            pos_title = round(height * 1/6)
            pos_desc = round(height * 1/2)
            
            res += width * '*' + '\n'
            for i in range(height - 2):
                if (i == pos_title):
                    res += '*' + Style.BRIGHT + (self.__name + " by " + self.__seller).center(width - 2) + Style.NORMAL + '*\n'
                    if self.discount:
                        res += '*' + Style.DIM + (str(self.__cost) + ' / ' + str(round(self.__cost * (1 - self.discount/100)))).center(width - 2)  + Style.NORMAL + '*\n'
                    else:
                        res += '*' + Style.DIM + str(self.__cost).center(width - 2) + Style.NORMAL + '*\n'

                elif (i == pos_desc):
                    res += '*' + Style.BRIGHT + "Decscription:".center(width-2) + '*\n' + Style.NORMAL; 

                    w_cnt = len(self.__desc)
                    if w_cnt > width - 4:
                        pos = 0
                        for j in range(height - 2 - i):
                            res += '* '
                            if w_cnt < width - 4:
                                res += self.__desc[pos:].center(width - 3) + '*\n' 
                                break
                            else:
                                res += self.__desc[pos:pos+width-4]
                                pos += width-4
                                w_cnt -= width - 4
                            res += ' *\n'
                    else:
                        res += '*' + self.__desc.center(width - 2) + '*\n'
                else:
                    res += '*' + ((width - 2) * ' ') + '*\n'
            res += width * '*' + '\n'
            write(fd, style.encode() + color.encode() + res.encode())
            write(fd, Fore.RESET.encode())

    #override methods
    def __eq__(self, value):
        if (self.__id == value.__id):
            return True
        return False
    def __str__(self):
        if self.__top_item:
            return f"Product: {self.__name} by {self.__seller}, cost: {self.__cost}, size: {self.__size}, description: {self.__desc}, discount: {self.__top_item[1]}, discount date: {self.__top_item[2]}"
        return f"Product: {self.__name} by {self.__seller}, cost: {self.__cost}, size: {self.__size}, description: {self.__desc}"
    def __repr__(self):
        if self.__top_item:
            return f"Product(name={self.__name}, seller={self.__seller}, cost={self.__cost}, size={self.__size}, desctiption={self.__desc}, history={self.__histoty})"
        return f"Product(name={self.__name}, seller={self.__seller}, cost={self.__cost}, size={self.__size}, description={self.__desc})"

