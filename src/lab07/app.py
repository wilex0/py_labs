from typing import List, Optional, Callable, Any, Dict
from base import *
from exceptions import *


class ProductApp:
    def __init__(self, collection: Optional[FunctionalProductCollection] = None):
        """
        Инициализация приложения.
        """
        self._collection = collection if collection else FunctionalProductCollection([])
    
    @property
    def collection(self) -> FunctionalProductCollection:
        """Возвращает коллекцию товаров."""
        return self._collection
    
    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в коллекцию.
        """
        try:
            existing = self.find_by_id(product.id)
            if existing:
                raise DuplicateItemError(f"Товар с ID {product.id} уже существует")
        except ItemNotFoundError:
            pass
        
        self._collection.append(product)
    
    def remove_product(self, product_id: int, confirm: bool = False) -> bool:
        """
        Удаляет товар из коллекции по ID.
        """
        product = self.find_by_id(product_id)
        if not confirm:
            return False
        
        self._collection.remove(product)
        return True
    
    def find_by_id(self, product_id: int) -> Product:
        """
        Поиск товара по ID.
        """
        product = self._collection.find_by_id(product_id)
        if product is None:
            raise ItemNotFoundError(f"Товар с ID {product_id} не найден")
        return product
    
    def find_by_name(self, name: str) -> List[Product]:
        """
        Поиск товаров по имени (частичное совпадение).
        """
        name_lower = name.lower()
        return [p for p in self._collection.get_all() if name_lower in p.name.lower()]
    
    def find_by_seller(self, seller: str) -> List[Product]:
        """
        Поиск товаров по продавцу.
        """
        seller_lower = seller.lower()
        return [p for p in self._collection.get_all() if seller_lower in p.seller.lower()]
    
    def filter_by_cost(self, max_cost: int) -> FunctionalProductCollection:
        """
        Фильтрация товаров по максимальной цене.
        """
        # Используем filter_by из FunctionalProductCollection
        return self._collection.filter_by(make_cost_filter(max_cost))
    
    def filter_by_quantity(self, min_q: int, max_q: int) -> FunctionalProductCollection:
        """
        Фильтрация товаров по диапазону количества.
        """
        from base import make_quantity_filter
        return self._collection.filter_by(make_quantity_filter(min_q, max_q))
    
    def filter_available(self) -> FunctionalProductCollection:
        """Фильтрация доступных товаров (quantity > 0)."""
        from base import is_available
        return self._collection.filter_by(is_available)
    
    def filter_with_discount(self) -> FunctionalProductCollection:
        """Фильтрация товаров со скидкой."""
        from base import has_discount
        return self._collection.filter_by(has_discount)
    
    def filter_food(self) -> FunctionalProductCollection:
        """Фильтрация продуктов питания."""
        from base import is_food
        return self._collection.filter_by(is_food)
    
    def filter_digital(self) -> FunctionalProductCollection:
        """Фильтрация цифровых товаров."""
        from base import is_digital
        return self._collection.filter_by(is_digital)
    
    def sort_by(self, key_func: Callable[[Product], Any], reverse: bool = False) -> 'ProductApp':
        """
        Сортировка коллекции.
        """
        self._collection.sort_by(key_func, reverse)
        return self
    
    def get_all_products(self) -> List[Product]:
        """Возвращает список всех товаров."""
        return self._collection.get_all()
    
    def get_product_count(self) -> int:
        """Возвращает количество товаров в коллекции."""
        return len(self._collection)
    
    def apply_discount_to_product(self, product_id: int, percent: int) -> None:
        """
        Применяет скидку к товару.
        """
        if not (0 < percent < 100):
            raise InvalidDataError("Процент скидки должен быть от 1 до 99")
        
        product = self.find_by_id(product_id)
        from datetime import datetime
        product.push_discount(percent, datetime.now())
    
    def buy_product(self, product_id: int, quantity: int) -> int:
        """
        Покупка товара.
        """
        product = self.find_by_id(product_id)
        
        if quantity > product.quantity:
            raise ValueError(f"Недостаточно товара. Доступно: {product.quantity}")
        
        total = product.curr_cost * quantity
        product.buy(quantity)
        return total
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по коллекции.
        """
        products = self._collection.get_all()
        if not products:
            return {
                "total_products": 0,
                "total_value": 0,
                "total_discount_saved": 0,
                "avg_cost": 0,
                "products_with_discount": 0
            }
        
        return {
            "total_products": len(products),
            "total_value": self._collection.total_cost(),
            "total_discount_saved": self._collection.total_discount_saved(),
            "avg_cost": self._collection.average_cost(),
            "products_with_discount": len(self.filter_with_discount().get_all())
        }
    
    def update_food_products(self) -> None:
        """Обновляет скидки для всех продуктов питания."""
        for product in self._collection.get_all():
            if isinstance(product, FoodProduct):
                product.update()
    
    def update_digital_products(self) -> None:
        """Обновляет скидки для всех цифровых продуктов."""
        for product in self._collection.get_all():
            if isinstance(product, DigitalProduct):
                product.update()