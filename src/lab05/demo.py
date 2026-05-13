# demo.py
from datetime import datetime, timedelta, date
from models import Product, FoodProduct, DigitalProduct, Size
from collection import FunctionalProductCollection
from strategies import *


def create_products() -> FunctionalProductCollection:
    """Создаёт тестовую коллекцию продуктов"""
    col = FunctionalProductCollection()
    
    # Обычные продукты
    col.append(Product(1000, "Ноутбук", "TechStore", 5, "Мощный ноутбук", Size.BIG))
    col.append(Product(500, "Мышь", "TechStore", 20, "Беспроводная мышь", Size.SMALL))
    col.append(Product(2000, "Монитор", "DisplayShop", 3, "4K монитор", Size.BIG))
    col.append(Product(50, "Блокнот", "OfficeMart", 100, "Тетрадь", Size.SMALL))
    col.append(Product(300, "Наушники", "TechStore", 0, "Беспроводные наушники", Size.NORMAL))
    col.append(Product(1500, "Клавиатура", "TechStore", 7, "Механическая клавиатура", Size.NORMAL))
    col.append(Product(80, "Ручка", "OfficeMart", 200, "Шариковая ручка", Size.SMALL))
    
    # Продукты питания
    exp_date1 = date.today() + timedelta(days=10)
    food1 = FoodProduct(150, "Йогурт", "FreshFood", 50, "Натуральный йогурт", Size.SMALL, exp_date1)
    food1.storage_temp = 4
    food1.add_expire_discount(10, 15)
    food1.add_expire_discount(5, 30)
    food1.add_expire_discount(2, 50)
    col.append(food1)
    
    exp_date2 = date.today() + timedelta(days=3)
    food2 = FoodProduct(80, "Хлеб", "Bakery", 30, "Свежий ржаной хлеб", Size.NORMAL, exp_date2)
    food2.add_expire_discount(3, 20)
    food2.add_expire_discount(1, 40)
    col.append(food2)
    
    exp_date3 = date.today() - timedelta(days=5)
    food3 = FoodProduct(100, "Молоко", "FreshFood", 2, "Пастеризованное молоко", Size.SMALL, exp_date3)
    col.append(food3)
    
    # Цифровые продукты
    digital1 = DigitalProduct(999, "Photoshop", "Adobe", 9999, "Редактор изображений", Size.NORMAL)
    digital1.add_review("Отлично!", 5.0)
    digital1.add_review("Хорошо", 4.5)
    digital1.add_review("Неплохо", 4.0)
    digital1.add_rating_discount(4.5, 15)
    digital1.add_rating_discount(4.8, 25)
    col.append(digital1)
    
    digital2 = DigitalProduct(499, "Spotify", "Spotify", 10000, "Музыкальный сервис", Size.SMALL)
    digital2.add_review("Супер!", 4.9)
    digital2.add_review("Отличный сервис", 4.7)
    digital2.add_rating_discount(4.5, 10)
    digital2.add_rating_discount(4.8, 20)
    col.append(digital2)
    
    digital3 = DigitalProduct(199, "VPN", "SecureNet", 5000, "VPN сервис", Size.NORMAL)
    digital3.add_review("Неплохо", 3.8)
    col.append(digital3)
    
    # Применяем ручные скидки
    col[0].push_discount(10, datetime(2020,2,10))  # Ноутбук -10%
    col[2].push_discount(5, datetime(2020,2,10))   # Монитор -5%
    col[5].push_discount(8, datetime(2020,2,10))   # Клавиатура -8%
    
    return col


def print_section(title: str):
    """Выводит заголовок раздела"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_subsection(title: str):
    """Выводит подзаголовок"""
    print(f"\n--- {title} ---")


# ==================== ДЕМОНСТРАЦИОННЫЕ ФУНКЦИИ ====================

def demo_sorting():
    """Демонстрация сортировок"""
    print_section("СЦЕНАРИЙ 1: СОРТИРОВКИ")
    
    products = create_products()
    
    print_subsection("Сортировка по названию")
    products.sort_by(by_name)
    for i, p in enumerate(products, 1):
        print(f"  {i}. {p.name}")
    
    print_subsection("Сортировка по цене (возрастание)")
    products.sort_by(by_curr_cost)
    for p in products:
        print(f"  {p.name}: ${p.curr_cost}")
    
    print_subsection("Сортировка по скидке (убывание)")
    products.sort_by(by_discount, reverse=True)
    for p in products.filter_by(has_discount):
        print(f"  {p.name}: скидка {p.discount}%")
    
    print_subsection("Сортировка по продавцу, затем по названию")
    products.sort_by(lambda p: (p.seller, p.name))
    for p in products:
        print(f"  {p.seller} - {p.name}")


def demo_filtering():
    """Демонстрация фильтрации"""
    print_section("СЦЕНАРИЙ 2: ФИЛЬТРАЦИЯ")
    
    products = create_products()
    
    print_subsection("Только доступные товары (количество > 0)")
    available = products.filter_by(is_available)
    print(f"  Найдено: {len(available)} товаров")
    for p in available:
        print(f"  {p.name}: {p.quantity} шт.")
    
    print_subsection("Только товары со скидкой")
    discounted = products.filter_by(has_discount)
    for p in discounted:
        print(f"  {p.name}: ${p.cost} => ${p.curr_cost} (скидка {p.discount}%)")
    
    print_subsection("Только продукты питания")
    for p in products.filter_by(is_food):
        status = "ПРОСРОЧЕН" if p.is_expired() else f"годен до {p.expiration_date}"
        print(f"  {p.name}: {status}")
    
    print_subsection("Только цифровые продукты")
    for p in products.filter_by(is_digital):
        print(f"  {p.name}: рейтинг {p.rating}")


def demo_factories():
    """Демонстрация фабрик функций"""
    print_section("СЦЕНАРИЙ 3: ФАБРИКИ ФУНКЦИЙ")
    
    products = create_products()
    
    print_subsection("Фильтр через make_cost_filter (цена <= 500)")
    cheap_filter = make_cost_filter(500)
    for p in products.filter_by(cheap_filter):
        print(f"  {p.name}: ${p.curr_cost}")
    
    print_subsection("Фильтр через make_quantity_filter (5-50 шт.)")
    stock_filter = make_quantity_filter(5, 50)
    for p in products.filter_by(stock_filter):
        print(f"  {p.name}: {p.quantity} шт.")
    
    print_subsection("Применение скидки через make_discount_applier")
    applier = make_discount_applier(10)
    test_products = products.filter_by(is_available).take(3)
    test_products.apply(applier)
    for p in test_products:
        print(f"  {p.name}: новая скидка {p.discount}%")


def demo_chaining():
    """Демонстрация цепочек методов"""
    print_section("СЦЕНАРИЙ 4: ЦЕПОЧКИ МЕТОДОВ")
    
    products = create_products()
    
    print_subsection("Цепочка: filter_by => sort_by")
    result = (products
              .filter_by(is_available)
              .sort_by(by_curr_cost))
    for p in result:
        print(f"  {p.name}: ${p.curr_cost} (в наличии: {p.quantity})")
    
    print_subsection("Цепочка: filter_by => filter_by => sort_by")
    result2 = (products
               .filter_by(is_food)
               .filter_by(has_discount)
               .sort_by(by_discount, reverse=True))
    for p in result2:
        print(f"  {p.name}: скидка {p.discount}%")
    
    print_subsection("Цепочка: filter_by => apply => sort_by")
    result3 = (products
               .filter_by(is_available)
               .take(4)
               .apply(lambda p: p.push_discount(5, datetime(2026,11,3)))
               .sort_by(by_discount, reverse=True))
    for p in result3:
        print(f"  {p.name}: скидка {p.discount}%")


def demo_map():
    """Демонстрация map"""
    print_section("СЦЕНАРИЙ 5: MAP И LAMBDA")
    
    products = create_products()
    
    print_subsection("Извлечение названий")
    names = products.map(lambda p: p.name)
    print(f"  {names[:8]}...")
    
    print_subsection("Извлечение (имя, цена, скидка)")
    info = products.map(lambda p: (p.name, p.curr_cost, p.discount))
    for name, cost, disc in info[:6]:
        disc_str = f", скидка {disc}%" if disc else ""
        print(f"  {name}: ${cost}{disc_str}")
    
    print_subsection("Форматирование строк")
    formatted = products.map(lambda p: f"[{p.seller}] {p.name}: ${p.curr_cost}")
    for f in formatted[:5]:
        print(f"  {f}")
    
    print_subsection("Извлечение ID")
    ids = products.map(lambda p: p.id)
    print(f"  ID: {ids}")


def demo_reduce():
    """Демонстрация reduce и агрегации"""
    print_section("СЦЕНАРИЙ 6: REDUCE И АГРЕГАЦИЯ")
    
    products = create_products()
    
    print_subsection("Общая стоимость")
    total = products.reduce(lambda acc, p: acc + p.curr_cost, 0)
    print(f"  Результат: ${total}")
    print(f"  Метод total_cost(): ${products.total_cost()}")
    
    print_subsection("Средняя цена")
    avg = products.reduce(lambda acc, p: acc + p.curr_cost, 0) / len(products)
    print(f"  Результат: ${avg:.2f}")
    print(f"  Метод average_cost(): ${products.average_cost():.2f}")
    
    print_subsection("Максимальная цена")
    max_price = products.reduce(lambda acc, p: max(acc, p.curr_cost), 0)
    print(f"  Максимальная цена: ${max_price}")
    
    print_subsection("Количество товаров со скидкой")
    discounted_count = products.reduce(lambda acc, p: acc + (1 if p.discount > 0 else 0), 0)
    print(f"  Товаров со скидкой: {discounted_count}")
    
    print_subsection("Общая экономия от скидок")
    total_saved = products.total_discount_saved()
    print(f"  Общая экономия: ${total_saved}")


def demo_discount_strategy():
    """Демонстрация стратегии скидки DiscountStrategy"""
    print_section("СЦЕНАРИЙ 7: DISCOUNT STRATEGY")
    
    products = create_products()
    
    print_subsection("Базовое применение")
    strategy = DiscountStrategy(15)
    test_product = products[0]
    print(f"  До: {test_product.name}, скидка {test_product.discount}%")
    strategy(test_product)
    print(f"  После: скидка {test_product.discount}%")
    
    print_subsection("Изменение процента")
    strategy.percent = 30
    strategy(test_product, datetime(2026,12,13))
    print(f"  Ещё раз: скидка {test_product.discount}%")
    print(f"  Текущая стратегия: {strategy}")
    
    print_subsection("Применение ко всей коллекции")
    strategy2 = DiscountStrategy(12)
    print("  Применяем скидку 12% ко всем доступным товарам:")
    available_products = products.filter_by(is_available)
    strategy2.apply_to_collection(available_products, datetime(2027, 2, 13))
    for p in available_products.take(5):
        print(f"    {p.name}: скидка {p.discount}%")


def demo_print_strategy():
    """Демонстрация стратегии печати PrintStrategy"""
    print_section("СЦЕНАРИЙ 8: PRINT STRATEGY")
    
    products = create_products()
    sample = products.filter_by(is_available).take(4)
    
    print_subsection("Краткий режим (verbose=False)")
    printer = PrintStrategy(verbose=False)
    printer.print_all(sample)
    
    print_subsection("Подробный режим (verbose=True)")
    printer.verbose = True
    printer.print_all(sample)
    
    print_subsection("Вывод отдельного продукта")
    single = sample.first()
    print(f"  Кратко: {PrintStrategy(verbose=False)(single)}")
    print(f"  Подробно: {PrintStrategy(verbose=True)(single)}")


def demo_update_strategy():
    """Демонстрация стратегии обновления UpdateStrategy"""
    print_section("СЦЕНАРИЙ 9: UPDATE STRATEGY")
    
    # Создаём свежую коллекцию
    fresh_products = create_products()
    
    print_subsection("Состояние ДО обновления")
    print("\n  Скидки у продуктов питания:")
    for p in fresh_products.filter_by(is_food):
        print(f"    {p.name}: скидка {p.discount}% (годен до {p.expiration_date})")
    
    print("\n  Скидки у цифровых продуктов:")
    for p in fresh_products.filter_by(is_digital):
        print(f"    {p.name}: скидка {p.discount}% (рейтинг {p.rating})")
    
    print_subsection("Применение update_collection()")
    updater = UpdateStrategy()
    changed = updater.update_collection(fresh_products)
    print(f"  Обновлено продуктов: {changed}")
    
    print_subsection("Состояние ПОСЛЕ обновления")
    print("\n  Скидки у продуктов питания:")
    for p in fresh_products.filter_by(is_food):
        print(f"    {p.name}: скидка {p.discount}%")
    
    print("\n  Скидки у цифровых продуктов:")
    for p in fresh_products.filter_by(is_digital):
        print(f"    {p.name}: скидка {p.discount}%")
    
    print_subsection("Повторное обновление (ничего не меняется)")
    changed2 = updater.update_collection(fresh_products)
    print(f"  Обновлено продуктов: {changed2}")


def demo_collection_methods():
    """Демонстрация новых методов коллекции"""
    print_section("СЦЕНАРИЙ 10: НОВЫЕ МЕТОДЫ КОЛЛЕКЦИИ")
    
    products = create_products()
    
    print_subsection("first() - первый элемент")
    print(f"  Первый продукт: {products.first().name}")
    
    print_subsection("first(predicate) - первый со скидкой")
    first_discounted = products.first(has_discount)
    print(f"  Первый продукт со скидкой: {first_discounted.name} (скидка {first_discounted.discount}%)")
    
    print_subsection("last() - последний элемент")
    print(f"  Последний продукт: {products.last().name}")
    
    print_subsection("take(n) - первые n элементов")
    for p in products.take(3):
        print(f"  {p.name}")
    
    print_subsection("skip(n) - пропустить n элементов")
    for p in products.skip(5).take(3):
        print(f"  {p.name}")
    
    print_subsection("distinct_by - уникальные продавцы")
    unique_sellers = products.distinct_by(lambda p: p.seller)
    for p in unique_sellers:
        print(f"  {p.seller}: {p.name}")


def demo_any_all():
    """Демонстрация any и all"""
    print_section("СЦЕНАРИЙ 11: ANY И ALL")
    
    products = create_products()
    
    print_subsection("Проверка any()")
    print(f"  Есть товары со скидкой? {products.any(has_discount)}")
    print(f"  Есть доступные товары? {products.any(is_available)}")
    print(f"  Есть цифровые продукты? {products.any(is_digital)}")
    print(f"  Есть просроченные продукты? {products.any(lambda p: is_food(p) and p.is_expired())}")
    
    print_subsection("Проверка all()")
    print(f"  Все товары доступны? {products.all(is_available)}")
    print(f"  Все доступные товары? {products.filter_by(is_available).all(is_available)}")
    print(f"  Все продукты питания свежие? {products.filter_by(is_food).all(lambda p: not p.is_expired())}")


def main():
    """Главная функция, запускающая все демонстрации"""
    print("\n" + "*" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №5: Функции как аргументы. Стратегии и делегаты.")
    print("*" * 70)
    
    # Запуск всех демонстраций
    demo_sorting()
    demo_filtering()
    demo_factories()
    demo_chaining()
    demo_map()
    demo_reduce()
    demo_discount_strategy()
    demo_print_strategy()
    demo_update_strategy()
    demo_collection_methods()
    demo_any_all()
    
if __name__ == "__main__":
    main()