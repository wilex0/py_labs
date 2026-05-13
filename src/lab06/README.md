# Лабораторная работа №6: Generics и typing

## Цель работы
Освоить аннотации типов, Generic-классы, TypeVar, структурную типизацию через Protocol.

## Реализованные компоненты

### Аннотации типов 
Все классы (`Product`, `FoodProduct`, `DigitalProduct`) получили полные аннотации параметров, возвращаемых значений и атрибутов.

### Generic-коллекция `TypedCollection[T]`
- Хранит элементы любого типа `T`
- Методы: `add`, `remove`, `get_all`, `size`, `is_empty`, `clear`, `contains`
- Поддержка итерации и `len()`

### Методы высшего порядка с TypeVar 
- `find(predicate: Callable[[T], bool]) -> Optional[T]` – поиск первого элемента по условию
- `filter(predicate: Callable[[T], bool]) -> list[T]` – фильтрация элементов
- `map(transform: Callable[[T], R]) -> list[R]` – преобразование элементов с возможной сменой типа результата

### Protocols и bound TypeVar 
- `Displayable` – требует метод `__str__() -> str`
- `Scorable` – требует свойство `rating -> float`
- `TypedCollection[D]` с `bound=Displayable` – может хранить любые объекты, у которых есть `__str__()`, **без явного наследования**
- `TypedCollection[S]` с `bound=Scorable` – может хранить любые объекты, у которых есть свойство `rating`, **без явного наследования**

## Демонстрация работы

### Сценарий 1: Generic коллекция TypedCollection

![Generic коллекция](../../images/lab06/1.png)

*Создание типизированной коллекции для продуктов, добавление и удаление элементов.*

**Что показано:**
- Создание `TypedCollection[Product]`
- Добавление продуктов разных типов
- Проверка размера коллекции и наличия элементов
- Удаление элемента

### Сценарий 2: Методы find, filter, map

![Методы высшего порядка](../../images/lab06/2.png)

*Демонстрация работы find, filter и map с разными типами преобразований.*

**Что показано:**
- `find()` – успешный поиск и возврат `None` при отсутствии
- `filter()` – фильтрация по продавцу
- `map()` – преобразование типов:
  - `Product` => `str` (имена)
  - `Product` => `int` (цены)
  - `Product` => `float` (цены с налогом)

### Сценарий 3: Protocol Displayable

![Protocol Displayable](../../images/lab06/3.png)

*Демонстрация работы TypedCollection с ограничением Displayable.*

**Что показано:**
- `FoodProduct` и `DigitalProduct` **не наследуются** от `Displayable`
- Но оба имеют метод `__str__()`, поэтому подходят под протокол
- Успешное добавление в `TypedCollection[Displayable]`
- Вызов метода `__str__()` через протокол для каждого элемента
- Фильтрация элементов по типу внутри коллекции с протоколом

### Сценарий 4: Protocol Scorable

![Protocol Scorable](../../images/lab06/4.png)

*Демонстрация работы TypedCollection с ограничением Scorable.*

**Что показано:**
- `DigitalProduct` **не наследуется** от `Scorable`
- Но имеет свойство `rating`, поэтому подходит под протокол
- Успешное добавление в `TypedCollection[Scorable]`
- Доступ к свойству `rating` через протокол
- Поиск и фильтрация с использованием `rating`
- Преобразование типов через `map()`

## Структура проекта
