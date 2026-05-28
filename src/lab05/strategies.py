from typing import Callable, List
from models import Product, FoodProduct, DigitalProduct, Size
from datetime import datetime

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