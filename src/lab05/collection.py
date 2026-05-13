# collection.py
from typing import Callable, List, Any
from functools import reduce
from models import Product, ProductCollection


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