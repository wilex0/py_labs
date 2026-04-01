from 

class ProductCollection:
    _DEFAULT_CAP = 10

    @property
    def head(self):
        return self.__head

    def __init__(self, capacity:int):
        if not capacity:
            capacity = ProductCollection._DEFAULT_CAP
        self.__items = [None] * capacity
