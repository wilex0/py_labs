import sys
from datetime import date
from pathlib import Path

from base import Product, Size, FoodProduct, DigitalProduct
from container import TypedCollection, Displayable, Scorable, D, S


def print_separator(title: str = "") -> None:
    """Печатает разделитель с заголовком"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    else:
        print("=" * 70)


def demo_generic_collection() -> None:
    """Сценарий 1: Generic коллекция TypedCollection (задание на 3)"""
    print_separator("СЦЕНАРИЙ 1: Generic коллекция TypedCollection")
    
    products: TypedCollection[Product] = TypedCollection()
    
    print("\nAdding products to collection:")
    p1 = Product(100, "Phone", "TechStore", 10, "Smartphone", Size.NORMAL)
    p2 = Product(50, "Charger", "TechStore", 30, "USB-C cable", Size.SMALL)
    p3 = Product(300, "Laptop", "TechStore", 5, "Gaming laptop", Size.BIG)
    
    products.add(p1)
    products.add(p2)
    products.add(p3)
    
    print(f"\nCollection statistics:")
    print(f"  Size: {products.size()}")
    print(f"  Empty: {products.is_empty()}")
    print(f"  Contains Phone? {products.contains(p1)}")
    
    products.remove(p2)
    print(f"  Size after removal: {products.size()}")


def demo_find_filter_map() -> None:
    """Сценарий 2: Методы find, filter, map (задание на 4)"""
    print_separator("СЦЕНАРИЙ 2: Методы find, filter, map")
    
    products: TypedCollection[Product] = TypedCollection()
    
    products.add(Product(100, "Phone", "TechStore", 10, "Smartphone", Size.NORMAL))
    products.add(Product(50, "Charger", "GadgetShop", 30, "USB-C cable", Size.SMALL))
    products.add(Product(300, "Laptop", "TechStore", 5, "Gaming laptop", Size.BIG))
    products.add(Product(25, "Case", "AccessoryStore", 20, "Phone case", Size.SMALL))
    products.add(Product(150, "Headphones", "AudioShop", 15, "Wireless", Size.NORMAL))
    
    print("\nMethod find():")
    tech_product = products.find(lambda p: p.seller == "TechStore")
    print(f"  First product from TechStore: {tech_product.name if tech_product else 'Not found'}")
    
    fake_product = products.find(lambda p: p.seller == "NonExistent")
    print(f"  Search for non-existent seller: {fake_product if fake_product else 'None'}")
    
    print("\nMethod filter():")
    tech_products = products.filter(lambda p: p.seller == "TechStore")
    print(f"  Products from TechStore ({len(tech_products)}):")
    for p in tech_products:
        print(f"     - {p.name} (${p.cost})")
    
    print("\nMethod map() - type transformation:")
    names: list[str] = products.map(lambda p: p.name)
    print(f"  Product names (list[str]): {names}")
    
    prices: list[int] = products.map(lambda p: p.cost)
    print(f"  Product prices (list[int]): {prices}")
    
    prices_with_tax: list[float] = products.map(lambda p: p.cost * 1.2)
    print(f"  Prices with 20% tax (list[float]): {[f'{x:.2f}' for x in prices_with_tax]}")


def demo_protocol_displayable() -> None:
    """
    Сценарий 3: Protocol Displayable
    """
    print_separator("СЦЕНАРИЙ 3: Protocol Displayable")
    
    # Создаем коллекцию с ограничением Displayable (объекты должны иметь __str__)
    # FoodProduct и DigitalProduct не наследуются от Displayable, но подходят!
    displayable_items: TypedCollection[Displayable] = TypedCollection()
    
    # Создаем FoodProduct (имеет __str__)
    milk = FoodProduct(
        cost=50,
        name="Milk",
        seller="FreshFarm",
        quantity=100,
        description="Fresh cow milk",
        size=Size.SMALL,
        expiration_date=date(2024, 12, 31)
    )
    
    bread = FoodProduct(
        cost=30,
        name="Bread",
        seller="Bakery",
        quantity=50,
        description="Fresh baked bread",
        size=Size.SMALL,
        expiration_date=date(2024, 11, 30)
    )
    
    # Создаем DigitalProduct (имеет __str__)
    ebook = DigitalProduct(
        cost=200,
        name="Programming Guide",
        seller="TechBooks",
        quantity=10,
        description="Learn Python programming",
        size=Size.NORMAL
    )
    
    software = DigitalProduct(
        cost=500,
        name="IDE Pro",
        seller="SoftCorp",
        quantity=5,
        description="Professional development environment",
        size=Size.BIG
    )
    
    print("\nAdding FoodProduct and DigitalProduct to Displayable collection:")
    print("(These classes do NOT inherit from Displayable, but they have __str__ method)")
    displayable_items.add(milk)
    displayable_items.add(bread)
    displayable_items.add(ebook)
    displayable_items.add(software)
    
    print(f"\nCollection size: {displayable_items.size()}")
    
    print("\nDisplaying all items (using __str__ method from Protocol):")
    for item in displayable_items.get_all():
        print(f"  {item}")
    
    print("\nFiltering displayable items by type:")
    food_items = displayable_items.filter(lambda x: 'FoodProduct' in str(type(x)))
    print(f"  Food products ({len(food_items)}):")
    for item in food_items:
        print(f"     {item}")
    
    digital_items = displayable_items.filter(lambda x: 'DigitalProduct' in str(type(x)))
    print(f"  Digital products ({len(digital_items)}):")
    for item in digital_items:
        print(f"     {item}")


def demo_protocol_scorable() -> None:
    """
    Сценарий 4: Protocol Scorable
    """
    print_separator("СЦЕНАРИЙ 4: Protocol Scorable")
    
    scorable_items: TypedCollection[Scorable] = TypedCollection()
    
    ebook1 = DigitalProduct(
        cost=150,
        name="Python Basics",
        seller="TechBooks",
        quantity=20,
        description="Learn Python from scratch",
        size=Size.NORMAL
    )
    ebook1.add_review("Great book!", 5)
    ebook1.add_review("Very helpful", 4.5)
    
    ebook2 = DigitalProduct(
        cost=250,
        name="Advanced Python",
        seller="TechBooks",
        quantity=15,
        description="Deep dive into Python",
        size=Size.NORMAL
    )
    ebook2.add_review("Excellent", 5)
    ebook2.add_review("Good content", 4)
    
    software = DigitalProduct(
        cost=500,
        name="Code Editor",
        seller="SoftCorp",
        quantity=8,
        description="Lightweight code editor",
        size=Size.BIG
    )
    software.add_review("Works great", 4.5)
    software.add_review("Fast and reliable", 4.8)
    
    print("\nAdding DigitalProduct to Scorable collection:")
    print("(DigitalProduct does NOT inherit from Scorable, but it has rating property)")
    scorable_items.add(ebook1)
    scorable_items.add(ebook2)
    scorable_items.add(software)
    
    print(f"\nCollection size: {scorable_items.size()}")
    
    print("\nItems with their ratings (using rating property from Protocol):")
    for item in scorable_items.get_all():
        print(f"  {item.name} -> Rating: {item.rating}/5.0")
    
    # Демонстрация find с использованием свойства протокола
    print("\nFinding items by rating:")
    high_rated = scorable_items.find(lambda x: x.rating >= 4.8)
    if high_rated:
        print(f"  Found high-rated item: {high_rated.name} (rating: {high_rated.rating})")
    
    # Демонстрация filter с использованием свойства протокола
    rated_above_4_5 = scorable_items.filter(lambda x: x.rating > 4.5)
    print(f"\nItems with rating > 4.5 ({len(rated_above_4_5)}):")
    for item in rated_above_4_5:
        print(f"  {item.name} -> Rating: {item.rating}")
    
    # Демонстрация map с преобразованием типов
    ratings = scorable_items.map(lambda x: x.rating)
    print(f"\nAll ratings (list[float]): {ratings}")
    
    names = scorable_items.map(lambda x: x.name)
    print(f"Product names (list[str]): {names}")


def main() -> None:
    """Главная функция демонстрации"""
    print("=" * 70)
    print("Generics и typing".center(70))
    print("=" * 70)
    
    demo_generic_collection()
    
    demo_find_filter_map()
    demo_protocol_displayable()
    demo_protocol_scorable()

if __name__ == "__main__":
    main()