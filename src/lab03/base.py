from enum import Enum
from re import sub
from datetime import datetime
from colorama import Fore, Style
import sys
from json import dumps, loads
from abc import ABC, abstractmethod
from models import *

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

    def apply_expire_discount(self):
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
        self.apply_expire_discount()
        if self.is_expired():
            print("You cannot buy an expired product")
            return None
        super().buy(quantity)
    def __str__(self):
        if self._top_item:
            return f"FoodProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self._size}, description: {self.description}, discount: {self._top_item[1]}, discount date: {self._top_item[2]}, days until expire: {self.get_days_until_expiry}"
        return f"FoodProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, days until expire: {self.get_days_until_expiry()}"

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

    def apply_rating_discount(self):
        if not len(self.__reviews_history) or not len(self.__discount_for_rating):
            return None
        d = sorted([i for i in self.__discount_for_rating.items() if self.__rating <= i[0]], key= lambda x: -x[1])[0][1]
        if d > self.discount:
            self.push_discount(d)

    def buy(self, quantity=1):
        self.apply_rating_discount()
        return super().buy(quantity)

    def __str__(self):
        if self._top_item:
            return f"DigitalProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, discount: {self._top_item[1]}, discount date: {self._top_item[2]}, rating: {self.rating}"
        return f"DigitalProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, rating: {self.rating}"