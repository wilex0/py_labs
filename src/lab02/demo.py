from collection import *
from models import Product

print("Сценарий 1 - базовые операции (добавление, удаление, len)")
p1 = Product(1000, "Ноутбук", "TechStore", 10, "Мощный игровой ноутбук", Size.BIG)
p2 = Product(500, "Смартфон", "MobileShop", 25, "Смартфон с отличной камерой", Size.NORMAL)
p3 = Product(50, "Мышь", "TechStore", 100, "Беспроводная мышь", Size.SMALL)
p4 = Product(200, "Клавиатура", "ComputerWorld", 30, "Механическая клавиатура", Size.NORMAL)

store = ProductCollection()

store.append(p1)
store.append(p2)
store.append(p3)
store.append(p4)

print("После добавления продуктов:")

print(f"\nКоличество продуктов через len(): {len(store)}")
print(f"{store}")

store.remove(p2)
print(f"После удаления смартфона:\n{store}")

store.remove_at(0)
print(f"После удаления по индексу 0:\n{store}")

print("Сценарий 2 - поиск и сортировка")
store.append(p1)
store.append(p2)

print("Поиск по имени (Ноутбук):")
found = store.find_by_name("Ноутбук")
if found:
    for p in found:
        print(f"Найден {p.name} продавца {p.seller} стоимостью {p.curr_cost}")

print("Поиск по размеру (Normal):")
found = store.find_by_size(Size.NORMAL)
if found:
    for p in found:
        print(f"  Найден: {p.name} (размер: {p.size})")

print("Поиск по цене (200-1000):")
found = store.find_by_cost(200, 1000)
if found:
    for p in found:
        print(f"  Найден: {p.name} - ${p.cost}")

print("Поиск по количеству (10-100):")
found = store.find_by_quantity(10, 100)
if found:
    for p in found:
        print(f"  {p.name}: {p.quantity} шт.")

print("Сортировка по имени (А-Я):")
store.sort_by_name()
print(f"Отсортирован по имени:\n{store}")
store.sort_by_cost()
print(f"Отсортирован по стоимости:\n{store}")
store.sort_by_quantity()
print(f"Отсортирован по количеству продукта:\n{store}")

print("Сценарий 3 - индексация и изменение состояния")
print("Доступ к первому элементу коллекции через индекс 0")
print(f"  store[0] == {store[0]}\n")
print(f"Покупка всех товаров у 1 и 3 объекта коллекции")
store[0].buy(10)
store[2].buy(30)
print("Получаем товары, которые находятся в наличии:")
has_q = store.get_has_quantity()
print(has_q)