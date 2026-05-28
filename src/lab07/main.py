import os
from colorama import *
from app import ProductApp
from cli import ConsoleCLI
from storage import save_collection, load_collection
from exceptions import StorageError
from base import *

init(autoreset=True)

FILE_NAME = os.path.dirname(os.path.abspath(__file__)) + "/products_data.json"

def main():
    try:
        collection = load_collection(FILE_NAME)
    except StorageError as e:
        print(f"Ошибка загрузки данных: {e}")
        print("Создана новая пустая коллекция")
        collection = FunctionalProductCollection([])

    app = ProductApp(collection)
    
    cli = ConsoleCLI(app)
    
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nПринудительное завершение...")
    finally:
        save_confirmation = input("\nСохранить изменения перед выходом? (y/n): ").lower()
        if save_confirmation == 'y':
            try:
                save_collection(app.collection, FILE_NAME)
                print("Данные сохранены успешно!")
            except StorageError as e:
                print(f"Ошибка сохранения: {e}")
        else:
            print("Изменения не сохранены")

if __name__ == "__main__":
    main()