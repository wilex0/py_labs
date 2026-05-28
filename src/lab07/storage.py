import json
import os
from datetime import datetime, date
from typing import Dict, Any
from base import *
from exceptions import StorageError

def product_to_dict(product: Product) -> Dict[str, Any]:
    """
    Преобразует объект Product в словарь для JSON-сериализации.
    """
    data: Dict[str, Any] = {
        "type": "Product",
        "id": product.id,
        "name": product.name,
        "seller": product.seller,
        "cost": product.cost,
        "quantity": product.quantity,
        "description": product.description,
        "size": product.size.value
    }
    
    if product.top_item:
        data["discount"] = product.top_item[1]
        data["last_discount_time"] = product.top_item[2].isoformat()
    
    if isinstance(product, FoodProduct):
        data["type"] = "FoodProduct"
        data["expiration_date"] = product.expiration_date.isoformat()
        if product.storage_temp is not None:
            data["storage_temp"] = product.storage_temp
        if product._FoodProduct__min_temp is not None:
            data["min_temp"] = product._FoodProduct__min_temp
        if product._FoodProduct__max_temp is not None:
            data["max_temp"] = product._FoodProduct__max_temp
        data["expire_discount"] = product.get_expire_discount()
    
    elif isinstance(product, DigitalProduct):
        data["type"] = "DigitalProduct"
        data["rating"] = product.rating
        data["reviews_history"] = product.get_reviews_history()
        data["rating_discount_history"] = product.get_rating_discount_history()
    
    return data


def dict_to_product(data: Dict[str, Any]) -> Product:
    """
    Преобразует словарь обратно в объект Product.
    """
    try:
        product_type = data.get("type", "Product")
        size = Size(data["size"])
        
        if product_type == "FoodProduct":
            expiration_date = date.fromisoformat(data["expiration_date"])
            product = FoodProduct(
                cost=data["cost"],
                name=data["name"],
                seller=data["seller"],
                quantity=data["quantity"],
                description=data["description"],
                size=size,
                expiration_date=expiration_date
            )
            if "storage_temp" in data and data["storage_temp"] is not None:
                product.storage_temp = data["storage_temp"]
            if "min_temp" in data and data["min_temp"] is not None:
                product._FoodProduct__min_temp = data["min_temp"]
            if "max_temp" in data and data["max_temp"] is not None:
                product.max_temp = data["max_temp"]
            if "expire_discount" in data:
                for days_str, disc in data["expire_discount"].items():
                    product.add_expire_discount(int(days_str), disc)
                    
        elif product_type == "DigitalProduct":
            product = DigitalProduct(
                cost=data["cost"],
                name=data["name"],
                seller=data["seller"],
                quantity=data["quantity"],
                description=data["description"],
                size=size
            )
            if "reviews_history" in data:
                for review, rating in data["reviews_history"]:
                    product.add_review(review, rating)
            if "rating_discount_history" in data:
                for rating_str, disc in data["rating_discount_history"].items():
                    product.add_rating_discount(float(rating_str), disc)
        else:
            product = Product(
                cost=data["cost"],
                name=data["name"],
                seller=data["seller"],
                quantity=data["quantity"],
                description=data["description"],
                size=size
            )
        
        product._Product__id = data["id"]
        if data["id"] >= Product._Product__Id:
            Product._Product__Id = data["id"]
        
        if "discount" in data and "last_discount_time" in data:
            discount_time = datetime.fromisoformat(data["last_discount_time"])
            product.push_discount(data["discount"], discount_time)
        
        return product
        
    except (KeyError, ValueError, TypeError) as e:
        raise StorageError(f"Ошибка преобразования данных: {e}")


def save_collection(collection, filepath: str) -> None:
    """
    Сохраняет коллекцию товаров в JSON-файл.
    """
    try:
        data = [product_to_dict(p) for p in collection.get_all()]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        raise StorageError(f"Ошибка записи в файл: {e}")


def load_collection(filepath: str):
    """
    Загружает коллекцию товаров из JSON-файла.
    """
    if not os.path.exists(filepath):
        return FunctionalProductCollection([])
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = [dict_to_product(item) for item in data]
        return FunctionalProductCollection(products)
        
    except json.JSONDecodeError as e:
        raise StorageError(f"Ошибка парсинга JSON: {e}")
    except IOError as e:
        raise StorageError(f"Ошибка чтения файла: {e}")