from datetime import date, datetime
from colorama import Fore, Style, init
from base import Product, ProductCollection, Size
from models import FoodProduct, DigitalProduct

init(autoreset=True)

def demonstrate_lab3():
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "СЦЕНАРИЙ 1: Создание объектов разных типов".center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()
    
    print(Fore.YELLOW + Style.BRIGHT + "1.1 Создание базового продукта (Product)")
    print(Fore.YELLOW + "-" * 40)
    basic_product = Product(
        cost=1500,
        name="Наушники",
        seller="AudioStore",
        quantity=10,
        description="Проводные наушники с микрофоном",
        size=Size.NORMAL
    )
    print(f"  {Fore.WHITE}{basic_product}")
    print()
    
    print(Fore.YELLOW + Style.BRIGHT + "1.2 Создание пищевого продукта (FoodProduct)")
    print(Fore.YELLOW + "-" * 40)
    food_product = FoodProduct(
        cost=250,
        name="Йогурт",
        seller="Молочный Двор",
        quantity=50,
        description="Натуральный йогурт с ягодами",
        size=Size.SMALL,
        expiration_date=date(2026, 5, 15)
    )
    food_product.storage_temp = 4
    food_product._FoodProduct__min_temp = 2
    food_product.max_temp = 6
    
    food_product.add_expire_discount(7, 15)
    food_product.add_expire_discount(3, 30)
    food_product.add_expire_discount(1, 50)
    
    print(f"  {Fore.WHITE}{food_product}")
    print(f"  Температура хранения: {food_product.storage_temp}C")
    print(f"  Диапазон температур: {food_product.min_temp}C - {food_product.max_temp}C")
    print(f"  Срок годности до: {food_product.expiration_date}")
    print(f"  Дней до истечения срока: {food_product.get_days_until_expiry()}")
    print(f"  Скидки за приближение срока: {food_product.get_expire_discount()}\n")
    
    print(Fore.YELLOW + Style.BRIGHT + "1.3 Создание цифрового продукта (DigitalProduct)")
    print(Fore.YELLOW + "-" * 40)
    digital_product = DigitalProduct(
        cost=2999,
        name="Онлайн-курс Python",
        seller="IT Academy",
        quantity=999,
        description="Полный курс по Python с нуля до профи",
        size=Size.NORMAL
    )
    digital_product.add_rating_discount(4.5, 10)
    digital_product.add_rating_discount(4.0, 20)
    digital_product.add_rating_discount(3.5, 30)
    
    digital_product.add_review("Отличный курс, всё понятно!", 5.0)
    digital_product.add_review("Хороший материал, но местами сложновато", 4.0)
    digital_product.add_review("Неплохо, но ожидал большего", 3.5)
    
    digital_product.add_rating_discount(4.7, 20)
    digital_product.add_rating_discount(3.2, 50)

    print(f"  {Fore.WHITE}{digital_product}")
    print(f"  Рейтинг: {digital_product.rating}/5.0")
    print(f"  Количество отзывов: {len(digital_product.get_reviews_history())}")
    print(f"  Скидки за рейтинг: {digital_product.get_rating_discount_history()}")
    
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "СЦЕНАРИЙ 2: Полиморфное поведение метода buy()".center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()
    
    products = [basic_product, food_product, digital_product]
    
    for i, product in enumerate(products, 1):
        print(Fore.YELLOW + Style.BRIGHT + f"2.{i} Покупка: {product.name}")
        print(Fore.YELLOW + "-" * 40)
        
        if isinstance(product, FoodProduct):
            print(f"  {Fore.MAGENTA}Тип: Пищевой продукт")
            if product.is_expired():
                print(f"  {Fore.RED}Продукт просрочен!")
            else:
                print(f"  {Fore.GREEN}Продукт свежий")
        elif isinstance(product, DigitalProduct):
            print(f"  {Fore.MAGENTA}Тип: Цифровой продукт")
            print(f"  Текущий рейтинг: {product.rating}")
        else:
            print(f"  {Fore.MAGENTA}Тип: Обычный продукт")
        
        try:
            product.buy(2)
        except ValueError as e:
            print(f"  {Fore.RED}Ошибка: {e}")
        print()
    
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "СЦЕНАРИЙ 3: Проверка типов через isinstance()".center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()
    
    test_objects = [basic_product, food_product, digital_product]
    
    for obj in test_objects:
        print(f"  Объект: {type(obj).__name__}")
        print(f"    Является Product? {Fore.GREEN if isinstance(obj, Product) else Fore.RED}{isinstance(obj, Product)}")
        print(f"    Является FoodProduct? {Fore.GREEN if isinstance(obj, FoodProduct) else Fore.RED}{isinstance(obj, FoodProduct)}")
        print(f"    Является DigitalProduct? {Fore.GREEN if isinstance(obj, DigitalProduct) else Fore.RED}{isinstance(obj, DigitalProduct)}")
        print()
    
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "СЦЕНАРИЙ 4: Интеграция с ProductCollection".center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()
    
    collection = ProductCollection()
    
    products_to_add = [
        Product(1000, "Книга", "Буквоед", 5, "Художественная литература", Size.NORMAL),
        FoodProduct(150, "Молоко", "Простоквашино", 30, "Пастеризованное 3.2%", Size.NORMAL, date(2026, 4, 25)),
        DigitalProduct(5000, "Антивирус", "Kaspersky", 100, "Защита на 1 год", Size.SMALL),
        FoodProduct(80, "Хлеб", "Хлебозавод", 20, "Ржаной хлеб", Size.NORMAL, date(2026, 4, 20)),
        DigitalProduct(1500, "Электронная книга", "ЛитРес", 50, "Бестселлер в PDF", Size.SMALL),
        Product(5000, "Стол", "IKEA", 3, "Письменный стол", Size.BIG),
        FoodProduct(300, "Сыр", "Сыроварня", 15, "Пармезан", Size.SMALL, date(2026, 6, 1)),
        DigitalProduct(999, "Подписка Spotify", "Spotify", 200, "Премиум на месяц", Size.SMALL),
    ]
    
    print(Fore.YELLOW + Style.BRIGHT + "4.1 Добавление продуктов в коллекцию")
    print(Fore.YELLOW + "-" * 40)
    for p in products_to_add:
        try:
            collection.append(p)
            type_name = type(p).__name__
            print(f"  {Fore.GREEN}Добавлен: {p.name} ({type_name})")
        except ValueError as e:
            print(f"  {Fore.RED}Ошибка: {e}")
    
    print(f"\n  Всего продуктов в коллекции: {len(collection)}")
    print(f"    Статистика по коллекции:")
    f = len([p for p in collection if isinstance(p, FoodProduct)])
    d = len([p for p in collection if isinstance(p, DigitalProduct)])

    print(f"    Объектов FoodProduct: {f}")
    print(f"    Объектов DigitalProduct: {d}")
    print(f"    Объектов базового класса Product: {len(collection) - (f + d)}")
    
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "СЦЕНАРИЙ 5: Фильтрация по типу и полиморфизм".center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()
    
    print(Fore.YELLOW + Style.BRIGHT + "5.1 Фильтрация продуктов по типу")
    print(Fore.YELLOW + "-" * 40)
    
    food_products = [p for p in collection if isinstance(p, FoodProduct)]
    print(f"  {Fore.GREEN}Пищевые продукты:")
    for i, p in enumerate(food_products, 1):
        days = p.get_days_until_expiry()
        status = f"{Fore.GREEN}свежий" if not p.is_expired() else f"{Fore.RED}просрочен"
        print(f"    {i}. {p.name} - срок: {days} дней ({status})")
    
    digital_products = [p for p in collection if isinstance(p, DigitalProduct)]
    print(f"\n  {Fore.BLUE}Цифровые продукты:")
    for i, p in enumerate(digital_products, 1):
        print(f"    {i}. {p.name} - рейтинг: {p.rating}/5.0")
    
    basic_products = [p for p in collection if type(p) == Product]
    print(f"\n  {Fore.YELLOW}Базовые продукты:")
    for i, p in enumerate(basic_products, 1):
        print(f"    {i}. {p.name}")
    
    print()
    print(Fore.YELLOW + Style.BRIGHT + "5.2 Полиморфный вызов методов для всей коллекции")
    print(Fore.YELLOW + "-" * 40)
    
    print("  Применение скидок и проверка статуса для всех продуктов:")
    for p in collection:
        if isinstance(p, FoodProduct):
            p.update()
            status = "просрочен" if p.is_expired() else f"годен {p.get_days_until_expiry()} дн."
            print(f"    {Fore.MAGENTA}[Food] {p.name}: статус={status}, скидка={p.discount}%")
        elif isinstance(p, DigitalProduct):
            p.update()
            print(f"    {Fore.CYAN}[Digital] {p.name}: рейтинг={p.rating}, скидка={p.discount}%")
        else:
            print(f"    {Fore.WHITE}[Basic] {p.name}: цена={p.curr_cost}, скидка={p.discount}%")
    print()
    
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "СЦЕНАРИЙ 6: Сортировка и поиск в коллекции".center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()
    
    print(Fore.YELLOW + Style.BRIGHT + "6.1 Сортировка по названию")
    print(Fore.YELLOW + "-" * 40)
    collection.sort_by_name()
    for i, p in enumerate(collection, 1):
        print(f"  {i}. {p.name} - {p.curr_cost} руб.")
    
    print()
    print(Fore.YELLOW + Style.BRIGHT + "6.2 Поиск по диапазону цен (500-2000 руб.)")
    print(Fore.YELLOW + "-" * 40)
    found = collection.find_by_cost(500, 2000)
    if found:
        for p in found:
            print(f"  {p.name}: {p.curr_cost} руб. (тип: {type(p).__name__})")
    else:
        print("  Продукты не найдены")
    
    print()
    print(Fore.YELLOW + Style.BRIGHT + "6.3 Поиск по названию 'Молоко'")
    print(Fore.YELLOW + "-" * 40)
    found = collection.find_by_name("Молоко")
    if found:
        for p in found:
            print(f"  {p.name} от {p.seller}")
    else:
        print("  Продукт не найден")
    print()
    
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "СЦЕНАРИЙ 7: Специфические методы дочерних классов".center(60))
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()
    
    print(Fore.YELLOW + Style.BRIGHT + "7.1 Работа с FoodProduct")
    print(Fore.YELLOW + "-" * 40)
    yogurt = FoodProduct(200, "Греческий йогурт", "Danone", 40, "Без добавок", Size.SMALL, date(2026, 4, 30))
    yogurt.storage_temp = 5
    yogurt._FoodProduct__min_temp = 2
    yogurt.max_temp = 8
    
    print(f"  Продукт: {yogurt.name}")
    print(f"  Просрочен? {yogurt.is_expired()}")
    print(f"  Дней до истечения: {yogurt.get_days_until_expiry()}")
    
    print()
    print(Fore.YELLOW + Style.BRIGHT + "7.2 Работа с DigitalProduct")
    print(Fore.YELLOW + "-" * 40)
    course = DigitalProduct(4990, "Курс Data Science", "SkillFactory", 500, "Машинное обучение", Size.NORMAL)
    course.add_review("Превосходно!", 5.0)
    course.add_review("Хорошо", 4.0)
    course.add_review("Средне", 3.0)
    
    print(f"  Продукт: {course.name}")
    print(f"  Рейтинг: {course.rating}")
    print(f"  История отзывов:")
    for review, rating in course.get_reviews_history():
        print(f"    {rating} - \"{review}\"")
    print()


if __name__ == "__main__":
    demonstrate_lab3()