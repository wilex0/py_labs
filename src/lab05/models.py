from enum import Enum
from re import sub
from datetime import datetime, date
from colorama import Fore, Style
import sys
from json import dumps, loads
from abc import ABC, abstractmethod
from os import write

class Size(Enum):
    SMALL = 1
    NORMAL = 2
    BIG = 3
    def __str__(self):
        match(self):
            case Size.SMALL:
                return "Small"
            case Size.NORMAL:
                return "Normal"
            case Size.BIG:
                return "Big"

def validate_strs(name: str):
        if not isinstance(name, str):
            raise TypeError("Incorrect str type")
        if not len(name):
            raise ValueError("Incorrect str length")
def validate_vals(v: int):
        if not isinstance(v, int):
            raise TypeError("Incorrect value type")
        if v < 0:
            raise ValueError("Incorrect value")
def validate_size(size: Size):
        if not isinstance(size, Size):
            raise TypeError("Incorrect size type")
def validate_percent(perc: int):
        if not isinstance(perc, int):
            raise TypeError("Incorrect percent type")
        if not (0 < perc < 100):
              raise ValueError("Incorrect percent value")
def validate_date(date: datetime):
        if not isinstance(date, datetime):
            raise TypeError("Incorrect date type")

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
    def quantity(self):
        return self.__quantity
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
            return int(self.__cost * (1 - self.discount / 100))
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
        if (all(v is None for v in self.__history)):
            return 0
        return self.__top_item[1]
    @property
    def id(self):
        return self.__id
    @property
    def history(self):
        return [ i for i in self.__history if i != None]
    @property
    def top_item(self):
        if self.__top_item != None:
            return self.__top_item
    def __init__(self, cost:int, name:str, seller:str, quantity:int, description:str, size:Size):
        self.size = size
        self.name = name
        self.description = description
        self.seller = seller
        
        validate_vals(cost)
        self.__cost = cost

        validate_vals(quantity)
        self.__quantity = quantity

        self.__cur_ptr = 0
        self.__history = Product.__MAX_N_HISTORY * [None]
        self.__top_item = None

        self.__id = Product.__Id + 1
        Product.__Id += 1
    @classmethod
    def load_from_json(cls, json:str):
        res = loads(json)
        prod = cls(int(res["cost"]), res["name"], res["seller"], res["quantity"], res["description"], Size(res["size"]))
        prod.__id = res["id"]
        Product.__Id -= 1
        
        if "discount" in res.keys():
            prod.push_discount(int(res["discount"]), datetime.strptime(res["last_discount_time"], "%Y-%m-%d"))
        return prod
    def append_products(self, quantity:int):
        validate_vals(quantity)
        self.__quantity += quantity
        print(Fore.GREEN + f"successfully added {quantity}. Current quantity is {self.quantity}" + Fore.RESET)
    def buy(self, quantity:int):
        validate_vals(quantity)
        if (quantity > self.quantity):
            raise ValueError("insufficient quantity of product")
        while (True):
            ans = None
            total_price = self.curr_cost * quantity
            if self.discount:
                ans = input(f"do you really want to buy {quantity} of the {self.name} by {self.seller} with the total price {total_price} (with {self.discount}% discount) (y/n): ")
            else:
                ans = input(f"do you really want to buy {quantity} of the {self.name} by {self.seller} with the total price {total_price} (y/n): ")

            if ans in ['y', 'n']:
                if ans == 'y':
                    if quantity > 1:
                        print(Fore.GREEN + f"you have successfully purchased {quantity} of the {self.name} for {self.curr_cost * quantity}" + Fore.RESET)
                    else:
                        print(Fore.GREEN + f"you have successfully purchased a {self.name} for {self.curr_cost}" + Fore.RESET)
                    self.__quantity -= quantity
                else:
                    print(Fore.RED + f"operation cancelled" + Fore.RESET)
                break
    def __prefix_ptr(self, op):
        if not op in ('+', '-'):
            return None
        if op == '+':
            self.__cur_ptr = self.__cur_ptr + 1 if self.__cur_ptr != Product.__MAX_N_HISTORY - 1 else 0
        else:
            self.__cur_ptr = self.__cur_ptr - 1 if self.__cur_ptr != 0 else Product.__MAX_N_HISTORY - 1

        return self.__cur_ptr
    def push_discount(self, percent, time:datetime=datetime.now()):
        validate_percent(percent)
        validate_date(time)

        if self.__top_item is None or self.__top_item[2] < time:
            self.__history[self.__cur_ptr] = (self.__cost * (1 - percent / 100), percent, time)
            self.__top_item = self.__history[self.__cur_ptr]
            self.__prefix_ptr('+')
        else:
            raise ValueError(f"date from the past - {time}")

    def pop_discount(self):
        self.__prefix_ptr('-')
        self.__top_item = self.__history[self.__cur_ptr - 1]

    def clear_discount(self):
        for i in range(Product.__MAX_N_HISTORY):
            self.__history[i] = None
        self.__cur_ptr = 0
        self.__top_item = None
    def write_data(self, style:Style=Style.NORMAL, color: Fore=Fore.WHITE, width=50, height = 20, fd:int=sys.stdout.fileno()):
        if fd != sys.stdout.fileno():
            res = None
            if self.__history[self.__cur_ptr - 1] is None:
                res = { "name":self.__name, "id": self.__id, "quantity": self.quantity, "description":self.__desc, "seller": self.__seller, "cost": self.__cost, "size": self.__size.value }
            else:
                res = { "name":self.__name, "id": self.__id, "quantity": self.quantity, "description":self.__desc, "seller": self.__seller, "cost": self.__cost, "size": self.__size.value, "discount":self.__top_item[1], "last_discount_time": str(self.__top_item[2].date()) }
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
                    res += '*' + Style.DIM + (str(self.quantity) + ' ct').center(width - 2) + Style.NORMAL + '*\n'

                elif (i == pos_desc):
                    res += '*' + Style.BRIGHT + "Description:".center(width-2) + '*\n' + Style.NORMAL; 

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
    def print_history(self):
        if self.history == []:
            print(Fore.RED + "price history is empty" + Fore.RESET)
        for i, trp in enumerate(self.history):
            print(f"{i+1}. {trp[2].strftime("%d.%m.%Y")} => discount = {trp[1]}, current price = {trp[0]} price = {self.cost}")
    def __eq__(self, value):
        if not isinstance(value, Product):
            return False
        return self.__id == value.__id
    def __str__(self):
        if self.__top_item:
            return f"Product: {self.__name} by {self.__seller}, cost: {self.__cost}, quantity: {self.quantity}, size: {self.__size}, description: {self.__desc}, discount: {self.__top_item[1]}, discount date: {self.__top_item[2]}"
        return f"Product: {self.__name} by {self.__seller}, cost: {self.__cost}, quantity: {self.quantity}, size: {self.__size}, description: {self.__desc}"
    def __repr__(self):
        if self.__top_item:
            return f"Product(name={self.__name}, seller={self.__seller}, cost={self.__cost}, size={self.__size}, desctiption={self.__desc}, history={self.__history})"
        return f"Product(name={self.__name}, seller={self.__seller}, cost={self.__cost}, size={self.__size}, description={self.__desc})"

class FoodProduct(Product):
    def __validate_int(self, i):
        if not isinstance(i, int):
            raise TypeError("Incorrect value type")
    
    @property
    def storage_temp(self):
        return self.__storage_temp
    
    @storage_temp.setter
    def storage_temp(self, temp: int):
        self.__validate_int(temp)
        self.__storage_temp = temp

    @property
    def expiration_date(self):
        return self.__expiration_date

    @property
    def min_temp(self):
        return self.__min_temp
    
    @property
    def max_temp(self):
        return self.__min_temp
    
    @property
    def max_temp(self):
        return self.__max_temp

    @max_temp.setter
    def max_temp(self, temp:int):
        self.__validate_int(temp)
        if self.__max_temp != None and temp < self.__min_temp:
            raise ValueError("Incorrect value")
        self.__max_temp = temp

    def __init__(self, cost: int, name: str, seller: str, quantity: int, 
                 description: str, size: Size, expiration_date: date):
        super().__init__(cost, name, seller, quantity, description, size)
        self.__storage_temp = None
        self.__min_temp = None
        self.__max_temp = None

        self.__expiration_date = expiration_date
        self.__expire_discount = {}

    def is_expired(self) -> bool:
        if self.storage_temp and self.__min_temp and self.__max_temp:
            return date.today() > self.expiration_date or not (self.__min_temp <= self.storage_temp <= self.__max_temp)
        return date.today() > self.expiration_date

    def get_days_until_expiry(self) -> int:
        d = self.expiration_date - date.today()
        return max(0, d.days)

    def add_expire_discount(self, days_left, discount):
        validate_percent(discount)
        self.__expire_discount[days_left] = discount

    def get_expire_discount(self):
        return self.__expire_discount.copy()

    def update(self):
        if self.is_expired() or not len(self.__expire_discount):
            return None
        d = self.get_days_until_expiry()
        exp_dis = 0

        for i,v in self.__expire_discount.items():
            if d <= i and v > exp_dis:
                exp_dis = v
        if exp_dis and exp_dis > self.discount:
            self.push_discount(exp_dis)    
    
    def buy(self, quantity=1):
        self.update()
        if self.is_expired():
            print("You cannot buy an expired product")
            return None
        super().buy(quantity)
    def __str__(self):
        if self._top_item:
            return f"FoodProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self._size}, description: {self.description}, discount: {self._top_item[1]}, discount date: {self._top_item[2]}, days until expire: {self.get_days_until_expiry}"
        return f"FoodProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, days until expire: {self.get_days_until_expiry()}"
    def print_history(self):
        if len(self.__expire_discount):
            print("expire discount history:")
            for i,v in enumerate(self.__expire_discount.items()):
                print(f"{i+1}. {v[0]} - {v[1]}")
        return super().print_history()

class DigitalProduct(Product):
    def __validate_rating(self, v):
        if not isinstance(v, (int, float)):
            raise TypeError("Incorrect value type")
        if not ( 0.0 <= v <= 5.0 ):
            raise ValueError("Incorrect value")
    
    @property
    def rating(self):
        return self.__rating

    def __init__(self, cost: int, name: str, seller: str, quantity: int, 
                 description: str, size: Size):
        super().__init__(cost, name, seller, quantity, description, size)

        self.__rating = 0.0
        self.__reviews_history = [] # [ (review, rating), ... ]
        self.__discount_for_rating = {} # { less_than: discount, ... }

    def add_review(self, review, rating):
        self.__validate_rating(rating)
        validate_strs(review)
        self.__reviews_history.append((review, rating))
        self.__rating = round(sum([i[1] for i in self.__reviews_history]) / len(self.__reviews_history), 2)

    def add_rating_discount(self, rating, discount):
        self.__validate_rating(rating)
        self.__discount_for_rating[rating] = discount

    def get_reviews_history(self):
        return self.__reviews_history.copy()

    def get_rating_discount_history(self):
        return self.__discount_for_rating.copy()

    def update(self):
        if not len(self.__reviews_history) or not len(self.__discount_for_rating):
            return None
        d = sorted([i for i in self.__discount_for_rating.items() if self.__rating <= i[0]], key= lambda x: -x[1])[0][1]
        if d > self.discount:
            self.push_discount(d)

    def buy(self, quantity=1):
        self.update()
        return super().buy(quantity)

    def __str__(self):
        if self._top_item:
            return f"DigitalProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, discount: {self._top_item[1]}, discount date: {self._top_item[2]}, rating: {self.rating}"
        return f"DigitalProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, rating: {self.rating}"
    
    def print_history(self):
        if len(self.__reviews_history):
            print("review history:")
            for i,v in enumerate(self.__reviews_history):
                print(f"{i+1}. {v[0]} - {v[1]}")
        if len(self.__discount_for_rating):
            print("discount for rating history:")
            for i,v in enumerate(self.__discount_for_rating.items()):
                print(f"{i+1}. {v[0]} - {v[1]}")
        return super().print_history()


class ProductCollection:
    def __init__(self, arr=None):
        if arr:
            if not isinstance(arr, list):
                raise ValueError("Incorrect array type")
            for i in arr:
                self.__validate_product(i)
            self._items = arr.copy()
        else:
            self._items = []
    def append(self, p:Product):
        self.__validate_product(p)
        if (self.find_by_name(p.name) and self.find_by_seller(p.seller)) or self.find_by_id(p.id):
            raise ValueError("Can't add same product")
        self._items.append(p)
    def __iter__(self):
        return iter(self._items)
    def __len__(self):
        return len(self._items)
    def remove(self, p:Product):
        self.__validate_product(p)
        for i,v in enumerate(self._items):
            self.__validate_product(v)
            if v.id == p.id:
                self._items.pop(i)
    def __getitem__(self, i:int):
        validate_vals(i)
        if i < 0:
             i += len(self._items)
        if i < 0 or i >= len(self._items):
            raise IndexError("Index out of range")
        return self._items[i]

    def remove_at(self, i:int):
        validate_vals(i)
        del self._items[i]
    
    def get_all(self):
        return self._items.copy()
    
    def find_by_cost(self, min:int, max:int):
        validate_vals(min); validate_vals(max)
        res = [i for i in self._items if min <= i.curr_cost <= max]
        if not len(res):
            return None
        return ProductCollection(res)

    def find_by_quantity(self, min:int, max:int):
        validate_vals(min); validate_vals(max)
        res = [i for i in self._items if min <= i.quantity <= max]
        if not len(res):
            return None
        return ProductCollection(res)
    
    def find_by_name(self, name:str):
        validate_strs(name)
        res = [i for i in self._items if i.name.lower() == name.lower()]
        if not len(res):
            return None
        return ProductCollection(res)
    
    def find_by_size(self, size:Size):
        validate_size(size)
        res = [i for i in self._items if i.size == size]
        if not len(res):
            return None
        return ProductCollection(res)
    
    def find_by_seller(self, seller:str):
        validate_strs(seller)
        res = [i for i in self._items if i.seller == seller]
        if not len(res):
            return None
        return ProductCollection(res)

    def find_by_id(self, id:int):
        for i in self._items:
            if i.id == id:
                return i
        return None

    def sort_by_name(self, reverse=False):
        self._items.sort(key=lambda x: x.name, reverse=reverse)
    def sort_by_quantity(self, reverse=False):
        self._items.sort(key=lambda x: x.quantity, reverse=reverse)
    def sort_by_cost(self, reverse=False):
        self._items.sort(key=lambda x: x.cost, reverse=reverse)
    def sort_by_id(self, reverse=False):
        self._items.sort(key=lambda x: x.id, reverse=reverse)
    def sort_by_size(self, reverse=False):
        self._items.sort(key=lambda x: x.size, reverse=reverse)

    def filter(self, pred):
        n_list = ProductCollection()
        for i in self._items:
            if pred(i):
                n_list.append(i)
        return n_list
    
    def __str__(self):
        res = ""
        for i, v in enumerate(self._items):
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