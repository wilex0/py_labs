from typing import TypeVar, Generic, Callable, Optional, List, Protocol

class Displayable(Protocol):
    """Протокол для объектов, которые можно отобразить"""
    def __str__(self) -> str:
        ...

class Scorable(Protocol):
    """Протокол для объектов, которые имеют оценку/рейтинг"""
    @property
    def rating(self) -> float:
        ...


T = TypeVar('T')           # Для общей коллекции
R = TypeVar('R')           # Для map - преобразование к другому типу
D = TypeVar('D', bound=Displayable)  # Только объекты с __str__
S = TypeVar('S', bound=Scorable)     # Только объекты с rating

class TypedCollection(Generic[T]):
    def __init__(self) -> None:
        """Инициализация пустой коллекции"""
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        """Добавляет элемент в коллекцию"""
        self._items.append(item)
        print(f"  Added: {item}")
    
    def remove(self, item: T) -> bool:
        """Удаляет элемент из коллекции"""
        if item in self._items:
            self._items.remove(item)
            print(f"  Removed: {item}")
            return True
        print(f"  Item not found: {item}")
        return False
    
    def get_all(self) -> List[T]:
        """Возвращает копию всех элементов коллекции"""
        return list(self._items)
    
    def size(self) -> int:
        """Возвращает количество элементов в коллекции"""
        return len(self._items)
    
    def is_empty(self) -> bool:
        """Проверяет, пуста ли коллекция"""
        return len(self._items) == 0
    
    def clear(self) -> None:
        """Очищает коллекцию"""
        self._items.clear()
        print("Collection cleared")
    
    def contains(self, item: T) -> bool:
        """Проверяет, содержится ли элемент в коллекции"""
        return item in self._items
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Находит первый элемент, удовлетворяющий условию.
        """
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Возвращает список всех элементов, удовлетворяющих условию.
        """
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        """
        Применяет функцию преобразования к каждому элементу.
        Тип результата может отличаться от типа элементов коллекции.
        Returns:
            Список результатов преобразования
        """
        return [transform(item) for item in self._items]
    
    def __str__(self) -> str:
        return f"TypedCollection({self._items})"

