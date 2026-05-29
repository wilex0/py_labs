from enum import Enum
from re import sub
from datetime import date, datetime
from colorama import Fore, Style
import sys
from json import dumps, loads
from os import write
from typing import Optional, List, Tuple, Dict, Any, Union

class Size(Enum):
    SMALL = 1
    NORMAL = 2
    BIG = 3
    
    def __str__(self) -> str:
        match(self):
            case Size.SMALL:
                return "Small"
            case Size.NORMAL:
                return "Normal"
            case Size.BIG:
                return "Big"

def validate_strs(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("Incorrect str type")
    if not len(name):
        raise ValueError("Incorrect str length")

def validate_vals(v: int) -> None:
    if not isinstance(v, int):
        raise TypeError("Incorrect value type")
    if v <= 0:
        raise ValueError("Incorrect value")

def validate_size(size: Size) -> None:
    if not isinstance(size, Size):
        raise TypeError("Incorrect size type")

def validate_percent(perc: int) -> None:
    if not isinstance(perc, int):
        raise TypeError("Incorrect percent type")
    if not (0 < perc < 100):
        raise ValueError("Incorrect percent value")

def validate_date(date: datetime) -> None:
    if not isinstance(date, datetime):
        raise TypeError("Incorrect date type")

class Product:
    __MAX_N_HISTORY: int = 10
    __Id: int = 0

    @property
    def size(self) -> Size:
        return self.__size
    
    @size.setter
    def size(self, new_size: Size) -> None:
        validate_size(new_size)
        self.__size = new_size
    
    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def name(self) -> str:
        return self.__name 
    
    @name.setter
    def name(self, new_name: str) -> None:
        validate_strs(new_name)
        self.__name = sub(r'( )+', ' ', new_name.strip())
    
    @property
    def seller(self) -> str:
        return self.__seller
    
    @seller.setter
    def seller(self, new_seller: str) -> None:
        validate_strs(new_seller)
        self.__seller = new_seller

    @property 
    def cost(self) -> int:
        return self.__cost
    
    @property
    def curr_cost(self) -> int:
        if self.discount:
            return int(self.__cost * (1 - self.discount / 100))
        return self.__cost
        
    @property
    def description(self) -> str:
        return self.__desc

    @description.setter
    def description(self, new_desc: str) -> None:
        validate_strs(new_desc)
        self.__desc = new_desc
    
    @property
    def discount(self) -> int:
        if (all(v is None for v in self.__histoty)):
            return 0
        return self.__top_item[1] if self.__top_item else 0
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def history(self) -> List[Optional[Tuple[int, int, datetime]]]:
        return [i for i in self.__histoty if i is not None]

    @property
    def top_item(self) -> Optional[Tuple[int, int, datetime]]:
        if self.__top_item is not None:
            return self.__top_item
        return None

    def __init__(self, cost: int, name: str, seller: str, quantity: int, 
                 description: str, size: Size) -> None:
        self.size = size
        self.name = name
        self.description = description
        self.seller = seller
        
        validate_vals(cost)
        self.__cost: int = cost

        validate_vals(quantity)
        self.__quantity: int = quantity

        self.__cur_ptr: int = 0
        self.__histoty: List[Optional[Tuple[int, int, datetime]]] = Product.__MAX_N_HISTORY * [None]
        self.__top_item: Optional[Tuple[int, int, datetime]] = None

        self.__id: int = Product.__Id + 1
        Product.__Id += 1

    @classmethod
    def load_from_json(cls, json_str: str) -> 'Product':
        res: Dict[str, Any] = loads(json_str)
        prod = cls(int(res["cost"]), res["name"], res["seller"], 
                   res["quantity"], res["description"], Size(res["size"]))
        prod.__id = res["id"]
        Product.__Id -= 1
        
        if "discount" in res.keys():
            prod.push_discount(int(res["discount"]), datetime.strptime(res["last_discount_time"], "%Y-%m-%d"))
        return prod

    def append_products(self, quantity: int) -> None:
        validate_vals(quantity)
        self.__quantity += quantity
        print(Fore.GREEN + f"successfully added {quantity}. Current quantity is {self.quantity}" + Fore.RESET)

    def buy(self, quantity: int) -> None:
        validate_vals(quantity)
        if quantity > self.quantity:
            raise ValueError("insufficient quantity of product")
        while True:
            ans: Optional[str] = None
            total_price: int = self.curr_cost * quantity
            if self.discount:
                ans = input(f"Вы действительно хотите приобрести {self.name} в количество {quantity} от {self.seller} с суммарной стоимостью в {total_price} (скидка {self.discount}%) (y/n): ")
            else:
                ans = input(f"Вы действительно хотите приобрести {self.name} в количество {quantity} от {self.seller} с суммарной стоимостью в {total_price} (y/n): ")

            if ans in ['y', 'n']:
                if ans == 'y':
                    if quantity > 1:
                        print(Fore.GREEN + f"Вы успешно приобрели {self.name} в количестве {quantity} за {self.curr_cost * quantity}" + Fore.RESET)
                    else:
                        print(Fore.GREEN + f"Вы успешно приобрели {self.name} в количестве {quantity} за {self.curr_cost}" + Fore.RESET)
                    self.__quantity -= quantity
                else:
                    print(Fore.RED + f"Операция отменена" + Fore.RESET)
                break

    def __prefix_ptr(self, op: str) -> Optional[int]:
        if op not in ('+', '-'):
            return None
        if op == '+':
            self.__cur_ptr = self.__cur_ptr + 1 if self.__cur_ptr != Product.__MAX_N_HISTORY - 1 else 0
        else:
            self.__cur_ptr = self.__cur_ptr - 1 if self.__cur_ptr != 0 else Product.__MAX_N_HISTORY - 1
        return self.__cur_ptr

    def push_discount(self, percent: int, time: datetime = datetime.now()) -> None:
        validate_percent(percent)
        validate_date(time)

        if self.__top_item is None or self.__top_item[2] < time:
            self.__histoty[self.__cur_ptr] = (self.__cost * (1 - percent / 100), percent, time)
            self.__top_item = self.__histoty[self.__cur_ptr]
            self.__prefix_ptr('+')
        else:
            raise ValueError(f"date from the past - {time}")

    def pop_discount(self) -> None:
        self.__prefix_ptr('-')
        if self.__cur_ptr - 1 >= 0:
            self.__top_item = self.__histoty[self.__cur_ptr - 1]

    def clear_discount(self) -> None:
        for i in range(Product.__MAX_N_HISTORY):
            self.__histoty[i] = None
        self.__cur_ptr = 0
        self.__top_item = None

    def write_data(self, style: Style = Style.NORMAL, color: Fore = Fore.WHITE, 
                   width: int = 50, height: int = 20, fd: int = sys.stdout.fileno()) -> None:
        if fd != sys.stdout.fileno():
            res: Dict[str, Any] = {}
            if self.__histoty[self.__cur_ptr - 1] is None:
                res = {"name": self.__name, "id": self.__id, "quantity": self.quantity, 
                       "description": self.__desc, "seller": self.__seller, 
                       "cost": self.__cost, "size": self.__size.value}
            else:
                res = {"name": self.__name, "id": self.__id, "quantity": self.quantity, 
                       "description": self.__desc, "seller": self.__seller, 
                       "cost": self.__cost, "size": self.__size.value, 
                       "discount": self.__top_item[1], "last_discount_time": str(self.__top_item[2].date())}
            write(fd, dumps(res).encode())
        else:
            if len(self.name) > width - 2:
                width = len(self.name) + 20
            res = ''
            pos_title: int = round(height * 1/6)
            pos_desc: int = round(height * 1/2)
            
            res += width * '*' + '\n'
            for i in range(height - 2):
                if i == pos_title:
                    res += '*' + Style.BRIGHT + (self.__name + " by " + self.__seller).center(width - 2) + Style.NORMAL + '*\n'
                    if self.discount:
                        res += '*' + Style.DIM + (str(self.__cost) + ' / ' + str(round(self.__cost * (1 - self.discount/100)))).center(width - 2) + Style.NORMAL + '*\n'
                    else:
                        res += '*' + Style.DIM + str(self.__cost).center(width - 2) + Style.NORMAL + '*\n'
                    res += '*' + Style.DIM + (str(self.quantity) + ' ct').center(width - 2) + Style.NORMAL + '*\n'
                elif i == pos_desc:
                    res += '*' + Style.BRIGHT + "Description:".center(width-2) + '*\n' + Style.NORMAL
                    w_cnt: int = len(self.__desc)
                    if w_cnt > width - 4:
                        pos: int = 0
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

    def print_history(self) -> None:
        if self.history == []:
            print(Fore.RED + "price history is empty" + Fore.RESET)
        for i, trp in enumerate(self.history):
            print(f"{i+1}. {trp[2].strftime('%d.%m.%Y')} => discount = {trp[1]}, current price = {trp[0]} price = {self.cost}")

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Product):
            return False
        return self.__id == value.__id
    
    def __str__(self) -> str:
        if self.__top_item:
            return f"Product: {self.__name} by {self.__seller}, cost: {self.__cost}, quantity: {self.quantity}, size: {self.__size}, description: {self.__desc}, discount: {self.__top_item[1]}, discount date: {self.__top_item[2]}"
        return f"Product: {self.__name} by {self.__seller}, cost: {self.__cost}, quantity: {self.quantity}, size: {self.__size}, description: {self.__desc}"
    
    def __repr__(self) -> str:
        if self.__top_item:
            return f"Product(name={self.__name}, seller={self.__seller}, cost={self.__cost}, size={self.__size}, desctiption={self.__desc}, history={self.__histoty})"
        return f"Product(name={self.__name}, seller={self.__seller}, cost={self.__cost}, size={self.__size}, description={self.__desc})"

class FoodProduct(Product):
    def __validate_int(self, i: Any) -> None:
        if not isinstance(i, int):
            raise TypeError("Incorrect value type")
    
    @property
    def storage_temp(self) -> Optional[int]:
        return self.__storage_temp
    
    @storage_temp.setter
    def storage_temp(self, temp: int) -> None:
        self.__validate_int(temp)
        self.__storage_temp = temp

    @property
    def expiration_date(self) -> date:
        return self.__expiration_date

    @property
    def min_temp(self) -> Optional[int]:
        return self.__min_temp

    @property
    def max_temp(self) -> Optional[int]:
        return self.__max_temp

    @max_temp.setter
    def max_temp(self, temp: int) -> None:
        self.__validate_int(temp)
        if self.__max_temp is not None and temp < self.__min_temp:
            raise ValueError("Incorrect value")
        self.__max_temp = temp

    def __init__(self, cost: int, name: str, seller: str, quantity: int, 
                 description: str, size: Size, expiration_date: date) -> None:
        super().__init__(cost, name, seller, quantity, description, size)
        self.__storage_temp: Optional[int] = None
        self.__min_temp: Optional[int] = None
        self.__max_temp: Optional[int] = None
        self.__expiration_date: date = expiration_date
        self.__expire_discount: Dict[int, int] = {}

    def is_expired(self) -> bool:
        if self.storage_temp and self.__min_temp and self.__max_temp:
            return date.today() > self.expiration_date or not (self.__min_temp <= self.storage_temp <= self.__max_temp)
        return date.today() > self.expiration_date

    def get_days_until_expiry(self) -> int:
        d: int = (self.expiration_date - date.today()).days
        return max(0, d)

    def add_expire_discount(self, days_left: int, discount: int) -> None:
        validate_percent(discount)
        self.__expire_discount[days_left] = discount

    def get_expire_discount(self) -> Dict[int, int]:
        return self.__expire_discount.copy()

    def update(self) -> None:
        if self.is_expired() or not len(self.__expire_discount):
            return None
        d: int = self.get_days_until_expiry()
        exp_dis: int = 0

        for i, v in self.__expire_discount.items():
            if d <= i and v > exp_dis:
                exp_dis = v
        if exp_dis and exp_dis > self.discount:
            self.push_discount(exp_dis)
    
    def buy(self, quantity: int = 1) -> None:
        self.update()
        if self.is_expired():
            print("You cannot buy an expired product")
            return None
        super().buy(quantity)
    
    def __str__(self) -> str:
        if self._Product__top_item:
            return f"FoodProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, discount: {self._Product__top_item[1]}, discount date: {self._Product__top_item[2]}, days until expire: {self.get_days_until_expiry()}"
        return f"FoodProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, days until expire: {self.get_days_until_expiry()}"
    
    def print_history(self) -> None:
        if len(self.__expire_discount):
            print("expire discount history:")
            for i, v in enumerate(self.__expire_discount.items()):
                print(f"{i+1}. {v[0]} - {v[1]}")
        return super().print_history()

class DigitalProduct(Product):
    def __validate_rating(self, v: Union[int, float]) -> None:
        if not isinstance(v, (int, float)):
            raise TypeError("Incorrect value type")
        if not (0.0 <= v <= 5.0):
            raise ValueError("Incorrect value")
    
    @property
    def rating(self) -> float:
        return self.__rating

    def __init__(self, cost: int, name: str, seller: str, quantity: int, 
                 description: str, size: Size) -> None:
        super().__init__(cost, name, seller, quantity, description, size)
        self.__rating: float = 0.0
        self.__reviews_history: List[Tuple[str, float]] = []
        self.__discount_for_rating: Dict[float, int] = {}

    def add_review(self, review: str, rating: Union[int, float]) -> None:
        self.__validate_rating(rating)
        validate_strs(review)
        self.__reviews_history.append((review, float(rating)))
        self.__rating = round(sum([i[1] for i in self.__reviews_history]) / len(self.__reviews_history), 2)

    def add_rating_discount(self, rating: Union[int, float], discount: int) -> None:
        self.__validate_rating(rating)
        self.__discount_for_rating[float(rating)] = discount

    def get_reviews_history(self) -> List[Tuple[str, float]]:
        return self.__reviews_history.copy()

    def get_rating_discount_history(self) -> Dict[float, int]:
        return self.__discount_for_rating.copy()

    def update(self) -> None:
        if not len(self.__reviews_history) or not len(self.__discount_for_rating):
            return None
        eligible: List[Tuple[float, int]] = [(r, d) for r, d in self.__discount_for_rating.items() if self.__rating <= r]
        if eligible:
            d: int = sorted(eligible, key=lambda x: -x[1])[0][1]
            if d > self.discount:
                self.push_discount(d)

    def buy(self, quantity: int = 1) -> None:
        self.update()
        return super().buy(quantity)

    def __str__(self) -> str:
        if self._Product__top_item:
            return f"DigitalProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, discount: {self._Product__top_item[1]}, discount date: {self._Product__top_item[2]}, rating: {self.rating}"
        return f"DigitalProduct: {self.name} by {self.seller}, cost: {self.cost}, quantity: {self.quantity}, size: {self.size}, description: {self.description}, rating: {self.rating}"
    
    def print_history(self) -> None:
        if len(self.__reviews_history):
            print("review history:")
            for i, v in enumerate(self.__reviews_history):
                print(f"{i+1}. {v[0]} - {v[1]}")
        if len(self.__discount_for_rating):
            print("discount for rating history:")
            for i, v in enumerate(self.__discount_for_rating.items()):
                print(f"{i+1}. {v[0]} - {v[1]}")
        return super().print_history()

def by_name(p: Product) -> str:
    return p.name.lower()

def by_seller(p: Product) -> str:
    return p.seller.lower()

def by_cost(p: Product) -> int:
    return p.cost

def by_curr_cost(p: Product) -> int:
    return p.curr_cost

def by_quantity(p: Product) -> int:
    return p.quantity

def by_discount(p: Product) -> int:
    return p.discount

def by_id(p: Product) -> int:
    return p.id


def has_discount(p: Product) -> bool:
    return p.discount > 0

def is_available(p: Product) -> bool:
    return p.quantity > 0

def is_food(p: Product) -> bool:
    return isinstance(p, FoodProduct)

def is_digital(p: Product) -> bool:
    return isinstance(p, DigitalProduct)


def make_cost_filter(max_cost: int) -> Callable[[Product], bool]:
    """Создаёт фильтр по максимальной стоимости"""
    def cost_filter(p: Product) -> bool:
        return p.curr_cost <= max_cost
    return cost_filter

def make_quantity_filter(min_q: int, max_q: int) -> Callable[[Product], bool]:
    """Создаёт фильтр по диапазону количества"""
    def quantity_filter(p: Product) -> bool:
        return min_q <= p.quantity <= max_q
    return quantity_filter

def make_discount_applier(percent: int) -> Callable[[Product], None]:
    """Создаёт функцию для применения скидки"""
    def applier(p: Product) -> None:
        try:
            p.push_discount(percent)
        except Exception as e:
            print(f"Ошибка: {e}")
    return applier

class DiscountStrategy:
    """
    Стратегия применения скидки с изменяемым процентом.
    """
    
    def __init__(self, default_percent: int = 10):
        self._percent = default_percent
    
    @property
    def percent(self) -> int:
        return self._percent
    
    @percent.setter
    def percent(self, value: int) -> None:
        if not 1 <= value <= 99:
            raise ValueError("Скидка должна быть между 1 и 99 процентами")
        self._percent = value
    
    def __call__(self, product: Product, date: datetime=datetime.now()) -> None:
        """Применяет текущую скидку к продукту"""
        product.push_discount(self._percent, date)
    
    def apply_to_collection(self, collection, date: datetime = datetime.now()) -> None:
        """Применяет стратегию ко всем продуктам в коллекции"""
        for product in collection:
            self(product, date)
    
    def __str__(self) -> str:
        return f"DiscountStrategy({self._percent}%)"


class PrintStrategy:
    """
    Стратегия печати.
    """
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
    
    def __call__(self, product: Product) -> str:
        if self.verbose:
            return str(product)
        else:
            discount = f" (-{product.discount}%)" if product.discount > 0 else ""
            return f"{product.name}: ${product.curr_cost}{discount}"
    
    def print_all(self, collection) -> None:
        for i, p in enumerate(collection, 1):
            print(f"{i}. {self(p)}")


class UpdateStrategy:
    def __call__(self, product):
        if isinstance(product, FoodProduct) or isinstance(product, DigitalProduct):
            product.update()
    def update_collection(self, collection) -> int:
        """
        Обновляет все продукты в коллекции.
        """
        changed = 0
        for product in collection:
            if self(product):
                changed += 1
        return changed
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
    def __len__(self):
        return len(self._items)

class FunctionalProductCollection(ProductCollection):
    def __init__(self, arr=None):
        super().__init__(arr)
    
    def sort_by(self, key_func: Callable[[Product], Any], reverse: bool = False) -> 'FunctionalProductCollection':
        """
        Сортировка по стратегии (функции-ключу).
        Сортирует текущую коллекцию in-place и возвращает self.
        """
        self._items.sort(key=key_func, reverse=reverse)
        return self
    
    def filter_by(self, predicate: Callable[[Product], bool]) -> 'FunctionalProductCollection':
        """
        Фильтрация по предикату.
        Возвращает новую коллекцию с отфильтрованными элементами.
        """
        return FunctionalProductCollection([p for p in self._items if predicate(p)])
    
    def apply(self, func: Callable[[Product], None]) -> 'FunctionalProductCollection':
        """
        Применяет функцию ко всем элементам коллекции (in-place).
        Возвращает self для цепочек вызовов.
        """
        for product in self._items:
            func(product)
        return self
    
    def map(self, transform_func: Callable[[Product], Any]) -> List[Any]:
        """
        Преобразование коллекции через map().
        Возвращает список результатов преобразования.
        """
        return list(map(transform_func, self._items))
    
    def reduce(self, func: Callable[[Any, Product], Any], initial: Any = None) -> Any:
        """
        Свёртка коллекции (аналог functools.reduce).
        """
        if initial is None:
            if not self._items:
                raise ValueError("Cannot reduce empty collection without initial value")
            result = self._items[0]
            for item in self._items[1:]:
                result = func(result, item)
            return result
        else:
            return reduce(func, self._items, initial)
    
    def for_each(self, func: Callable[[Product], None]) -> 'FunctionalProductCollection':
        """
        Выполняет функцию для каждого элемента.
        Возвращает self для цепочек вызовов.
        """
        for product in self._items:
            func(product)
        return self
    
    def any(self, predicate: Callable[[Product], bool]) -> bool:
        """
        Проверяет, есть ли хотя бы один элемент, удовлетворяющий предикату.
        """
        return any(predicate(p) for p in self._items)
    
    def all(self, predicate: Callable[[Product], bool]) -> bool:
        """
        Проверяет, все ли элементы удовлетворяют предикату.
        """
        return all(predicate(p) for p in self._items)
    
    def total_cost(self) -> int:
        """
        Суммарная текущая стоимость всех продуктов.
        """
        return sum(p.curr_cost for p in self._items)
    
    def average_cost(self) -> float:
        """
        Средняя текущая стоимость продуктов.
        """
        if len(self._items) == 0:
            return 0.0
        return self.total_cost() / len(self._items)
    
    def total_discount_saved(self) -> int:
        """
        Общая сумма скидки по всем продуктам.
        """
        return sum(p.cost - p.curr_cost for p in self._items)
    
    def first(self, predicate: Callable[[Product], bool] = None) -> Product:
        """
        Возвращает первый элемент, удовлетворяющий предикату.
        Если предикат не указан, возвращает первый элемент.
        """
        if predicate is None:
            if not self._items:
                raise ValueError("Collection is empty")
            return self._items[0]
        
        for p in self._items:
            if predicate(p):
                return p
        raise ValueError("No element satisfies the predicate")
    
    def last(self, predicate: Callable[[Product], bool] = None) -> Product:
        """
        Возвращает последний элемент, удовлетворяющий предикату.
        Если предикат не указан, возвращает последний элемент.
        """
        if predicate is None:
            if not self._items:
                raise ValueError("Collection is empty")
            return self._items[-1]
        
        for p in reversed(self._items):
            if predicate(p):
                return p
        raise ValueError("No element satisfies the predicate")
    
    def take(self, n: int) -> 'FunctionalProductCollection':
        """Возвращает первые n элементов."""
        if n <= 0:
            return FunctionalProductCollection([])
        return FunctionalProductCollection(self._items[:n])
    
    def skip(self, n: int) -> 'FunctionalProductCollection':
        """Пропускает первые n элементов."""
        if n <= 0:
            return FunctionalProductCollection(self._items)
        return FunctionalProductCollection(self._items[n:])
    
    def distinct_by(self, key_func: Callable[[Product], Any]) -> 'FunctionalProductCollection':
        """
        Возвращает коллекцию с уникальными элементами по указанному ключу.
        """
        seen = set()
        result = []
        for p in self._items:
            key = key_func(p)
            if key not in seen:
                seen.add(key)
                result.append(p)
        return FunctionalProductCollection(result)
    def __len__(self):
        return super().__len__()