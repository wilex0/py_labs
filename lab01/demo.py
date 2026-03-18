from model import Product, Size
from os import *
from datetime import datetime
from colorama import Style, Fore

def demo_objects():
    p1 = Product(70_000, "Nikon Z 8 45.7MP", "sankaragopalak0", "The Nikon Z 8 45.7MP Mirrorless Digital Camera is a high-performance camera designed for photography enthusiasts. With a maximum aperture of f/1.2 and a 45.7 MP maximum resolution, this camera captures stunning, detailed images.", Size.SMALL)
    p1.push_discount(20)
    p1.push_discount(50, datetime(2030, 1,2))
    p1.push_discount(15, datetime(2040, 2, 1))
    p1.write_data(color=Fore.CYAN, width= 100)
    print("История скидок первого объекта:")
    print(p1.history)
    p2 = Product(20_000, "Nikon Z 23 45.7MP", "sacher", "The Nikon Z 23 45.7MP Mirrorless Digital Camera.", Size.SMALL)
    p2.write_data()
    p2.push_discount(10)
    print("Второго:")
    print(p2.history)

def demo_json_rdwr():
    p = Product(70_000, "Nikon Z 8 45.7MP", "sankaragopalak0", "The Nikon Z 8 45.7MP Mirrorless Digital Camera is a high-performance camera designed for photography enthusiasts. With a maximum aperture of f/1.2 and a 45.7 MP maximum resolution, this camera captures stunning, detailed images.", Size.SMALL)
    print("Записываемый объект:")
    p.write_data()
    fd = open("data", O_RDWR | O_CREAT | O_TRUNC)
    p.write_data(fd=fd) # запись объекта в файл
    lseek(fd, 0, SEEK_SET)
    stat = fstat(fd)

    p2 = Product.load_from_json(read(fd, stat.st_size).decode(encoding="utf-8")) # чтение объекта из файла и создание копии p
    print("Прочтенный объект:")
    p2.write_data()

    if (p2 == p):
        print("Изначальный объект равен новому")
    remove("data")

def demo_atrr_err():
    p2 = Product(20_000, "Nikon Z 8 45.7MP", "sankaragopalak0", "The Nikon Z 8 45.7MP Mirrorless Digital Camera is a high-performance camera designed for photography enthusiasts. With a maximum aperture of f/1.2 and a 45.7 MP maximum resolution, this camera captures stunning, detailed images.", Size.SMALL)
    try:
        print ("Установка скидки в 120%")
        p2.push_discount(120) # скидка в 120%
    except ValueError as e:
        print(f"{e}")

    try:
        print("Установка пустого имени")
        p2.name = '' # установка пустого названия продукта 
    except ValueError as e:
        print(f"{e}")

    try:
        print("Установка пустого описания")
        p2.description = ''
    except ValueError as e:
        print(f"{e}")

    try:
        print("Установка размера некорректоного типа (нужно перечисление)")
        p2.size = 2
    except TypeError as e:
        print(f"{e}")
    
    try:
        print("Добавление скики, дата добавления которой находится в прошлом относительно текущей даты")
        p2.push_discount(10) # datetime.now() текущий момент времени
        p2.push_discount(50, datetime(1999,1,2)) # скидка `из прошлого`
    except ValueError as e:
        print(f"{e}")

def demo_magic():
    p = Product(20_000, "Nikon Z 8 45.7MP", "sankaragopalak0", "The Nikon Z 8 45.7MP Mirrorless Digital Camera is a high-performance camera designed for photography enthusiasts. With a maximum aperture of f/1.2 and a 45.7 MP maximum resolution, this camera captures stunning, detailed images.", Size.SMALL)
    p.push_discount(44)
    print("метод __str__")
    print(str(p) + '\n')
    print("метод __repr__")
    print(p.__repr__() + '\n')
    print("метод __eq__")
    print("Сравнение обънетов выполняется через метод __eq__ и возмонжно только при одинаковых идентификаторах объетов, этот же сценарий возможен только при загрузки объекта из файла в json-форамте как было покано в сценарии 1")


demo_magic()