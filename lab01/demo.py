from model import Product, Size
from os import *
from datetime import datetime
from colorama import Style, Fore


#Создание объектов 
p = Product(70_000, "Nikon Z 8 45.7MP", "sankaragopalak0", "The Nikon Z 8 45.7MP Mirrorless Digital Camera is a high-performance camera designed for photography enthusiasts. With a maximum aperture of f/1.2 and a 45.7 MP maximum resolution, this camera captures stunning, detailed images.", Size.SMALL)
fd = open("data", O_RDWR | O_CREAT | O_TRUNC)
p.write_data(fd=fd) # запись объекта в файл
lseek(fd, 0, SEEK_SET)
stat = fstat(fd)

p2 = Product.load_from_json(read(fd, stat.st_size).decode(encoding="utf-8")) # чтение объекта из файла и создание копии p
remove("data")

if p == p2:
    print("Объект p == p2")
p2.write_data() # запись объекта в поток вывода

p2.push_discount(30) # установка скидки
p2.push_discount(40, datetime(2026,8,2))
p2.push_discount(50, datetime(2026,8,4))
print(p2)

p2.write_data()

print(repr(p2)) # __repr__

#Изменение свойств, обработка ошибок
try:
    p2.push_discount(120) # скидка в 120%
except ValueError as e:
    print(f"{e}")

try:
    p2.name = '' # установка пустого названия продукта 
except TypeError as e:
    print(f"{e}")

#Бизнес методы и состояния
p2.write_data(Style.NORMAL, Fore.CYAN, width=100, height=15) # записать в поток вывода используя предпочитаемый стиль

fd = open("data", O_WRONLY | O_CREAT)
p2.write_data(fd=fd) #запись в файл
close(fd)

print(p2.history) # история изменения скидки у объекта
p2.pop_discount() # удаление последней установленной скидки
print(p2.discount)
print(p2.cost)
print(p2.curr_cost)
print(p2.id)
print(p2.top_item)
