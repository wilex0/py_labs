from datetime import date, timedelta
from colorama import Fore, Style, init
from models import *
from interfaces import *

init(autoreset=True)


def print_scenario(num: int, title: str):
    print(f"\n{'='*70}")
    print(f"  СЦЕНАРИЙ {num}: {title}")
    print(f"{'='*70}{Style.RESET_ALL}\n")


# ============ ПОДГОТОВКА ТЕСТОВЫХ ДАННЫХ ============
print(f"{Fore.CYAN}Подготовка тестовых данных...{Style.RESET_ALL}")

milk_fresh = FoodProduct(
    cost=100, name="Milk 'Fresh Morning'", seller="DairyFarm", quantity=50,
    description="Fresh whole milk 1L from local farm", size=Size.NORMAL,
    expiration_date=date.today() + timedelta(days=10)
)
milk_fresh.storage_temp = 4
milk_fresh.min_temp = 2
milk_fresh.max_temp = 6
milk_fresh.add_expire_discount(days_left=3, discount=20)
milk_fresh.add_expire_discount(days_left=1, discount=50)

bread = FoodProduct(
    cost=50, name="Whole Grain Bread", seller="BakeryFresh", quantity=30,
    description="Freshly baked whole grain bread 500g", size=Size.NORMAL,
    expiration_date=date.today() + timedelta(days=2)
)
bread.add_expire_discount(days_left=1, discount=30)

cheese = FoodProduct(
    cost=200, name="Aged Cheddar", seller="DairyFarm", quantity=20,
    description="Premium aged cheddar cheese 200g", size=Size.SMALL,
    expiration_date=date.today() + timedelta(days=30)
)

yogurt_expired = FoodProduct(
    cost=80, name="Strawberry Yogurt", seller="DairyFarm", quantity=15,
    description="Strawberry yogurt 150ml", size=Size.SMALL,
    expiration_date=date.today() - timedelta(days=1)
)

python_course = DigitalProduct(
    cost=500, name="Python Masterclass", seller="EduOnline", quantity=1000,
    description="Complete Python programming course with projects", size=Size.BIG
)
python_course.add_review("Excellent course! Learned so much!", 5.0)
python_course.add_review("Very comprehensive and well structured", 4.5)
python_course.add_review("Good course but could use more examples", 4.0)
python_course.add_rating_discount(rating=4.0, discount=15)

photo_editor = DigitalProduct(
    cost=300, name="PhotoEditor Pro 2024", seller="SoftWarehouse", quantity=500,
    description="Professional photo editing software with AI features", size=Size.NORMAL
)
photo_editor.add_review("Best photo editor on the market!", 5.0)
photo_editor.add_review("Great features, intuitive interface", 4.8)
photo_editor.add_review("Good value for money", 4.5)

ebook_basic = DigitalProduct(
    cost=150, name="E-book: Python Basics", seller="BookWorld", quantity=2000,
    description="Introduction to Python programming for beginners", size=Size.SMALL
)
ebook_basic.add_review("Good for absolute beginners", 4.0)
ebook_basic.add_review("Could use more practical examples", 3.0)
ebook_basic.add_review("Decent introduction", 3.5)
ebook_basic.add_rating_discount(rating=3.5, discount=25)

notebook = Product(
    cost=30, name="Simple Notebook", seller="OfficeStore", quantity=100,
    description="Basic A5 notebook 48 sheets", size=Size.SMALL
)

pen = Product(
    cost=15, name="Ballpoint Pen", seller="OfficeStore", quantity=200,
    description="Blue ballpoint pen", size=Size.SMALL
)

collection = ProductCollection()
collection.append(milk_fresh)
collection.append(bread)
collection.append(cheese)
collection.append(yogurt_expired)
collection.append(python_course)
collection.append(photo_editor)
collection.append(ebook_basic)
collection.append(notebook)
collection.append(pen)

print(f"Создана коллекция из {len(collection)} продуктов")


# ============ СЦЕНАРИЙ 1: Фильтрация коллекции по интерфейсам ============
print_scenario(1, "Фильтрация коллекции по интерфейсам")

print(f"{Fore.GREEN}1.1 Получение печатных объектов через get_printable(){Style.RESET_ALL}")
printable_collection = collection.get_printable()
print(f"Найдено {len(printable_collection)} продуктов, реализующих Printable:")
printable_collection.print_all()

print(f"\n{Fore.GREEN}1.2 Получение обновляемых объектов через get_updatable(){Style.RESET_ALL}")
updatable_collection = collection.get_updatable()
print(f"Найдено {len(updatable_collection)} продуктов, реализующих Updatable:")
updatable_collection.print_all()

print(f"\n{Fore.GREEN}1.3 Получение сравнимых объектов через get_comparable(){Style.RESET_ALL}")
comparable_collection = collection.get_comparable()
print(f"Найдено {len(comparable_collection)} продуктов, реализующих Comparable:")
comparable_collection.print_all()

print(f"\n{Fore.GREEN}1.4 Проверка реализации интерфейсов через isinstance(){Style.RESET_ALL}")
for product in [milk_fresh, python_course]:
    interfaces = []
    if isinstance(product, Printable):
        interfaces.append("Printable")
    if isinstance(product, Updatable):
        interfaces.append("Updatable")
    if isinstance(product, Comparable):
        interfaces.append("Comparable")
    print(f"  {product.name}: {', '.join(interfaces)}")


# ============ СЦЕНАРИЙ 2: Массовое обновление объектов ============
print_scenario(2, "Массовое обновление объектов через интерфейс Updatable")

print(f"{Fore.GREEN}2.1 Состояние продуктов до обновления:{Style.RESET_ALL}")
updatable = collection.get_updatable()
for i, item in enumerate(updatable, 1):
    print(f"  {i}. {item.to_string()}")

print(f"\n{Fore.GREEN}2.2 Выполнение update_all()...{Style.RESET_ALL}")
collection.update_all()

print(f"\n{Fore.GREEN}2.3 Состояние продуктов после обновления:{Style.RESET_ALL}")
for i, item in enumerate(collection.get_updatable(), 1):
    print(f"  {i}. {item.to_string()}")

print(f"\n{Fore.GREEN}2.4 Разное поведение update() в разных классах:{Style.RESET_ALL}")
print(f"  FoodProduct '{milk_fresh.name}': обновляет скидку по сроку годности")
print(f"    Дней до истечения: {milk_fresh.get_days_until_expiry()}")
print(f"    Текущая скидка: {milk_fresh.discount}%")
print(f"  DigitalProduct '{python_course.name}': обновляет скидку по рейтингу")
print(f"    Рейтинг: {python_course.rating}")
print(f"    Текущая скидка: {python_course.discount}%")


# ============ СЦЕНАРИЙ 3: Сравнение объектов ============
print_scenario(3, "Сравнение объектов через интерфейс Comparable")

print(f"{Fore.GREEN}3.1 Сравнение продуктов питания (по свежести):{Style.RESET_ALL}")
print(f"  Свежее молоко (10 дней) vs Хлеб (2 дня):")
result = milk_fresh.compare_to(bread)
print(f"  milk_fresh.compare_to(bread) = {result} ", end="")
if result > 0:
    print(f"{Fore.GREEN}(молоко свежее){Style.RESET_ALL}")
elif result < 0:
    print(f"{Fore.RED}(хлеб свежее){Style.RESET_ALL}")
else:
    print(f"{Fore.YELLOW}(одинаковая свежесть){Style.RESET_ALL}")

print(f"\n  Сыр (30 дней) vs Молоко (10 дней):")
result = cheese.compare_to(milk_fresh)
print(f"  cheese.compare_to(milk_fresh) = {result} ", end="")
if result > 0:
    print(f"{Fore.GREEN}(сыр свежий){Style.RESET_ALL}")

print(f"\n  Молоко (10 дней) vs Просроченный йогурт:")
result = milk_fresh.compare_to(yogurt_expired)
print(f"  milk_fresh.compare_to(yogurt_expired) = {result} ", end="")
if result > 0:
    print(f"{Fore.GREEN}(молоко не просрочено){Style.RESET_ALL}")

print(f"\n{Fore.GREEN}3.2 Сравнение цифровых продуктов (по рейтингу):{Style.RESET_ALL}")
print(f"  Python курс (рейтинг {python_course.rating}) vs PhotoEditor (рейтинг {photo_editor.rating}):")
result = python_course.compare_to(photo_editor)
print(f"  python_course.compare_to(photo_editor) = {result} ", end="")
if result < 0:
    print(f"{Fore.RED}(Python курс имеет ниже рейтинг){Style.RESET_ALL}")
elif result > 0:
    print(f"{Fore.GREEN}(Python курс имеет выше рейтинг){Style.RESET_ALL}")

print(f"\n  PhotoEditor (рейтинг {photo_editor.rating}) vs E-book (рейтинг {ebook_basic.rating}):")
result = photo_editor.compare_to(ebook_basic)
print(f"  photo_editor.compare_to(ebook_basic) = {result} ", end="")
if result > 0:
    print(f"{Fore.GREEN}(PhotoEditor имеет выше рейтинг){Style.RESET_ALL}")

print(f"\n{Fore.GREEN}3.3 Попытка сравнения разных типов:{Style.RESET_ALL}")
print(f"  milk_fresh.compare_to(python_course):")
try:
    result = milk_fresh.compare_to(python_course)
    print(f"  Результат: {result}")
except TypeError as e:
    print(f"  {Fore.RED}TypeError: {e}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}(Ожидаемое поведение - разные типы не сравниваются){Style.RESET_ALL}")


# ============ СЦЕНАРИЙ 4: Сортировка коллекции ============
print_scenario(4, "Сортировка коллекции через интерфейс Comparable")

print(f"{Fore.GREEN}4.1 Сортировка всей коллекции:{Style.RESET_ALL}")
print(f"  До сортировки:")
collection.print_all()

collection.sort_by_comparable()

print(f"\n  После сортировки (от лучшего к худшему по группам):")
collection.print_all()

print(f"{Fore.GREEN}4.2 Поиск лучших и худших продуктов:{Style.RESET_ALL}")
best_list = collection.find_best()
worst_list = collection.find_worst()
if best_list:
    print(f"  Лучшие продукты:")
    for item in best_list:
        print(f"    {Fore.GREEN}{item.to_string()}{Style.RESET_ALL}")
if worst_list:
    print(f"  Худшие продукты:")
    for item in worst_list:
        print(f"    {Fore.RED}{item.to_string()}{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}4.3 Сортировка только продуктов питания:{Style.RESET_ALL}")
food_collection = collection.filter(lambda x: isinstance(x, FoodProduct))
print(f"  До сортировки:")
food_collection.print_all()
food_collection.sort_by_comparable()
print(f"  После сортировки (от свежего к просроченному):")
food_collection.print_all()

best_food_list = food_collection.find_best()
worst_food_list = food_collection.find_worst()
if best_food_list:
    for item in best_food_list:
        print(f"  {Fore.GREEN}Самый свежий: {item.to_string()}{Style.RESET_ALL}")
if worst_food_list:
    for item in worst_food_list:
        print(f"  {Fore.RED}Наименее свежий: {item.to_string()}{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}4.4 Сортировка только цифровых продуктов:{Style.RESET_ALL}")
digital_collection = collection.filter(lambda x: isinstance(x, DigitalProduct))
print(f"  До сортировки:")
digital_collection.print_all()
digital_collection.sort_by_comparable()
print(f"  После сортировки (от высокого рейтинга к низкому):")
digital_collection.print_all()

best_digital_list = digital_collection.find_best()
worst_digital_list = digital_collection.find_worst()
if best_digital_list:
    for item in best_digital_list:
        print(f"  {Fore.GREEN}Самый рейтинговый: {item.to_string()}{Style.RESET_ALL}")
if worst_digital_list:
    for item in worst_digital_list:
        print(f"  {Fore.RED}Наименее рейтинговый: {item.to_string()}{Style.RESET_ALL}")


# ============ СЦЕНАРИЙ 5: Полиморфизм через интерфейсы ============
print_scenario(5, "Полиморфизм через интерфейсы")

print(f"{Fore.GREEN}5.1 Вывод объектов через интерфейс Printable:{Style.RESET_ALL}")
for item in [milk_fresh, python_course]:
    if isinstance(item, Printable):
        print(f"    {item.to_string()}")

print(f"\n{Fore.GREEN}5.2 Обновление объектов через интерфейс Updatable:{Style.RESET_ALL}")
print(f"  Попытка обновления разных типов:")
milk_fresh.add_expire_discount(20, 30)
python_course.add_rating_discount(5, 40)
for item in [milk_fresh, python_course, notebook]:
    if isinstance(item, Updatable):
        old_discount = item.discount
        item.update()
        new_discount = item.discount
        print(f"    {item.name}: скидка изменилась с {old_discount}% на {new_discount}%")
    else:
        print(f"    {Fore.YELLOW}{item.name}: не реализует Updatable - пропускаем{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}5.3 Вывод истории через интерфейс Printable:{Style.RESET_ALL}")
for item in [milk_fresh, python_course]:
    if isinstance(item, Printable):
        print(f"История для '{item.name}':")
        item.print_history()