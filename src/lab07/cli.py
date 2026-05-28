from typing import Optional, List
from datetime import date, datetime
from colorama import Fore, Style, init

from base import *
from app import ProductApp
from exceptions import ItemNotFoundError, DuplicateItemError, InvalidDataError


init(autoreset=True)

class ConsoleCLI:
    def __init__(self, app: ProductApp):
        """
        Инициализация CLI.
        """
        self.app = app
        self.running = True
    
    def _print_header(self, text: str) -> None:
        """Печатает заголовок."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
        print(f"{text.center(60)}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}{Style.RESET_ALL}\n")
    
    def _print_success(self, text: str) -> None:
        """Печатает сообщение об успехе."""
        print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")
    
    def _print_error(self, text: str) -> None:
        """Печатает сообщение об ошибке."""
        print(f"{Fore.RED}{text}{Style.RESET_ALL}")
    
    def _print_info(self, text: str) -> None:
        """Печатает информационное сообщение."""
        print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")
    
    def _print_product_table(self, products: List[Product], title: str = "Товары") -> None:
        """
        Печатает таблицу товаров.
        """
        if not products:
            self._print_info("Нет товаров для отображения")
            return
        
        self._print_header(title)
        
        print(f"{Fore.CYAN}{'ID':<6} {'Название':<25} {'Продавец':<15} {'Цена':<10} {'Скидка':<8} {'Кол-во':<8}")
        print(f"{'-' * 80}{Style.RESET_ALL}")
        
        for p in products:
            discount_str = f"{p.discount}%" if p.discount else "-"
            if p.discount:
                color = Fore.GREEN
            elif p.quantity == 0:
                color = Fore.RED
            else:
                color = Fore.WHITE
            
            name_display = p.name[:24] + ".." if len(p.name) > 24 else p.name
            seller_display = p.seller[:13] + ".." if len(p.seller) > 13 else p.seller
            
            print(f"{color}{p.id:<6} {name_display:<25} {seller_display:<15} "
                  f"{p.curr_cost:<10} {discount_str:<8} {p.quantity:<8}{Style.RESET_ALL}")
        
        print()
    
    def _print_product_details(self, product: Product) -> None:
        """Печатает детальную информацию о товаре."""
        self._print_header(f"Информация о товаре #{product.id}")
        
        print(f"{Fore.YELLOW}Название:{Style.RESET_ALL} {product.name}")
        print(f"{Fore.YELLOW}Продавец:{Style.RESET_ALL} {product.seller}")
        print(f"{Fore.YELLOW}Описание:{Style.RESET_ALL} {product.description}")
        print(f"{Fore.YELLOW}Размер:{Style.RESET_ALL} {product.size}")
        print(f"{Fore.YELLOW}Количество:{Style.RESET_ALL} {product.quantity}")
        print(f"{Fore.YELLOW}Обычная цена:{Style.RESET_ALL} {product.cost}")
        print(f"{Fore.YELLOW}Текущая цена:{Style.RESET_ALL} {product.curr_cost}")
        
        if product.discount:
            print(f"{Fore.GREEN}Скидка:{Style.RESET_ALL} {product.discount}%")
            if product.top_item:
                print(f"{Fore.GREEN}Дата скидки:{Style.RESET_ALL} {product.top_item[2].strftime('%d.%m.%Y %H:%M')}")
        
        if isinstance(product, FoodProduct):
            print(f"\n{Fore.MAGENTA}--- Продукт питания ---{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Срок годности:{Style.RESET_ALL} {product.expiration_date.strftime('%d.%m.%Y')}")
            print(f"{Fore.YELLOW}Дней до истечения:{Style.RESET_ALL} {product.get_days_until_expiry()}")
            if product.storage_temp:
                print(f"{Fore.YELLOW}Температура хранения:{Style.RESET_ALL} {product.storage_temp}°C")
            if product.is_expired():
                self._print_error("Товар просрочен!")
        
        if isinstance(product, DigitalProduct):
            print(f"\n{Fore.MAGENTA}--- Цифровой продукт ---{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Рейтинг:{Style.RESET_ALL} {product.rating}/5.0")
        
        print()
    
    def _get_int_input(self, prompt: str, min_val: Optional[int] = None, 
                       max_val: Optional[int] = None, default: Optional[int] = None) -> Optional[int]:
        """
        Получает целочисленный ввод от пользователя.
        """
        while True:
            try:
                user_input = input(f"{prompt} (или 'q' для отмены): ").strip()
                if user_input.lower() == 'q':
                    return None
                
                if default is not None and user_input == '':
                    return default
                
                value = int(user_input)
                if min_val is not None and value < min_val:
                    self._print_error(f"Значение должно быть не менее {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    self._print_error(f"Значение должно быть не более {max_val}")
                    continue
                return value
            except ValueError:
                self._print_error("Пожалуйста, введите целое число")
    
    def _get_str_input(self, prompt: str, required: bool = True, default: str = "") -> Optional[str]:
        """
        Получает строковый ввод от пользователя.
        """
        while True:
            user_input = input(f"{prompt} (или 'q' для отмены): ").strip()
            if user_input.lower() == 'q':
                return None
            
            if user_input == '' and default:
                return default
            
            if required and user_input == '':
                self._print_error("Поле не может быть пустым")
                continue
            
            return user_input
    
    def _get_size_input(self) -> Optional[Size]:
        """Получает выбор размера от пользователя."""
        print("Выберите размер:")
        for size in Size:
            print(f"  {size.value}. {size}")
        
        choice = self._get_int_input("Ваш выбор", min_val=1, max_val=3)
        if choice is None:
            return None
        
        return Size(choice)
    
    def _get_date_input(self, prompt: str) -> Optional[date]:
        """Получает дату от пользователя."""
        while True:
            date_str = input(f"{prompt} (ГГГГ-ММ-ДД, или 'q' для отмены): ").strip()
            if date_str.lower() == 'q':
                return None
            
            try:
                return date.fromisoformat(date_str)
            except ValueError:
                self._print_error("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
    
    def menu_add_product(self) -> None:
        """Меню добавления товара."""
        self._print_header("Добавление нового товара")
        
        print("Тип товара:")
        print("  1. Обычный товар")
        print("  2. Продукт питания")
        print("  3. Цифровой товар")
        
        choice = self._get_int_input("Ваш выбор", min_val=1, max_val=3)
        if choice is None:
            return
        
        name = self._get_str_input("Название товара")
        if name is None:
            return
        
        seller = self._get_str_input("Продавец")
        if seller is None:
            return
        
        description = self._get_str_input("Описание")
        if description is None:
            return
        
        cost = self._get_int_input("Цена", min_val=1)
        if cost is None:
            return
        
        quantity = self._get_int_input("Количество", min_val=0)
        if quantity is None:
            return
        
        size = self._get_size_input()
        if size is None:
            return
        
        try:
            if choice == 2:
                exp_date = self._get_date_input("Дата истечения срока годности")
                if exp_date is None:
                    return
                
                product = FoodProduct(cost, name, seller, quantity, description, size, exp_date)
                
                add_temp = input("Добавить температуру хранения? (y/n): ").lower()
                if add_temp == 'y':
                    temp = self._get_int_input("Температура хранения")
                    if temp is not None:
                        product.storage_temp = temp
                
            elif choice == 3:  
                product = DigitalProduct(cost, name, seller, quantity, description, size)
            else:
                product = Product(cost, name, seller, quantity, description, size)
            
            self.app.add_product(product)
            self._print_success(f"Товар \"{name}\" успешно добавлен (ID: {product.id})")
            
        except DuplicateItemError as e:
            self._print_error(str(e))
        except Exception as e:
            self._print_error(f"Ошибка при создании товара: {e}")
    
    def menu_remove_product(self) -> None:
        """Меню удаления товара."""
        self._print_header("Удаление товара")
        
        product_id = self._get_int_input("ID товара для удаления", min_val=1)
        if product_id is None:
            return
        
        try:
            product = self.app.find_by_id(product_id)
            self._print_product_details(product)
            
            confirm = input(f"\n{Fore.RED}Вы уверены, что хотите удалить товар \"{product.name}\"? (y/n): {Style.RESET_ALL}").lower()
            if confirm == 'y':
                self.app.remove_product(product_id, confirm=True)
                self._print_success(f"Товар \"{product.name}\" успешно удалён")
            else:
                self._print_info("Удаление отменено")
                
        except ItemNotFoundError as e:
            self._print_error(str(e))
    
    def menu_show_all(self) -> None:
        """Показывает все товары."""
        products = self.app.get_all_products()
        self._print_product_table(products, "Все товары")
    
    def menu_show_available(self) -> None:
        """Показывает доступные товары."""
        filtered = self.app.filter_available()
        self._print_product_table(filtered.get_all(), "Доступные товары")
    
    def menu_show_with_discount(self) -> None:
        """Показывает товары со скидкой."""
        filtered = self.app.filter_with_discount()
        self._print_product_table(filtered.get_all(), "Товары со скидкой")
    
    def menu_search(self) -> None:
        """Меню поиска товаров."""
        self._print_header("Поиск товаров")
        
        print("Поиск по:")
        print("  1. ID товара")
        print("  2. Названию")
        print("  3. Продавцу")
        
        choice = self._get_int_input("Ваш выбор", min_val=1, max_val=3)
        if choice is None:
            return
        
        if choice == 1:
            product_id = self._get_int_input("Введите ID")
            if product_id is None:
                return
            try:
                product = self.app.find_by_id(product_id)
                self._print_product_details(product)
            except ItemNotFoundError as e:
                self._print_error(str(e))
        
        elif choice == 2:
            name = self._get_str_input("Введите название (или его часть)")
            if name is None:
                return
            products = self.app.find_by_name(name)
            self._print_product_table(products, f"Результаты поиска по названию: \"{name}\"")
        
        elif choice == 3:
            seller = self._get_str_input("Введите имя продавца (или его часть)")
            if seller is None:
                return
            products = self.app.find_by_seller(seller)
            self._print_product_table(products, f"Результаты поиска по продавцу: \"{seller}\"")
    
    def menu_filter(self) -> None:
        """Меню фильтрации товаров."""
        self._print_header("Фильтрация товаров")
        
        print("Фильтровать по:")
        print("  1. Максимальной цене")
        print("  2. Диапазону количества")
        print("  3. Типу (продукты питания)")
        print("  4. Типу (цифровые товары)")
        
        choice = self._get_int_input("Ваш выбор", min_val=1, max_val=4)
        if choice is None:
            return
        
        if choice == 1:
            max_cost = self._get_int_input("Максимальная цена", min_val=1)
            if max_cost is None:
                return
            filtered = self.app.filter_by_cost(max_cost)
            self._print_product_table(filtered.get_all(), f"Товары дешевле {max_cost}")
        
        elif choice == 2:
            min_q = self._get_int_input("Минимальное количество", min_val=0)
            if min_q is None:
                return
            max_q = self._get_int_input("Максимальное количество", min_val=min_q)
            if max_q is None:
                return
            filtered = self.app.filter_by_quantity(min_q, max_q)
            self._print_product_table(filtered.get_all(), f"Товары с количеством от {min_q} до {max_q}")
        
        elif choice == 3:
            filtered = self.app.filter_food()
            self._print_product_table(filtered.get_all(), "Продукты питания")
        
        elif choice == 4:
            filtered = self.app.filter_digital()
            self._print_product_table(filtered.get_all(), "Цифровые товары")
    
    def menu_sort(self) -> None:
        """Меню сортировки товаров."""
        self._print_header("Сортировка товаров")
        
        print("Сортировать по:")
        print("  1. Названию")
        print("  2. Продавцу")
        print("  3. Цене (обычной)")
        print("  4. Цене (со скидкой)")
        print("  5. Количеству")
        print("  6. Скидке")
        
        choice = self._get_int_input("Ваш выбор", min_val=1, max_val=6)
        if choice is None:
            return
        
        reverse = input("В обратном порядке? (y/n): ").lower() == 'y'
        
        key_map = {
            1: by_name,
            2: by_seller,
            3: by_cost,
            4: by_curr_cost,
            5: by_quantity,
            6: by_discount
        }
        
        self.app.sort_by(key_map[choice], reverse)
        self._print_success("Коллекция отсортирована")
        self.menu_show_all()
    
    def menu_buy_product(self) -> None:
        """Меню покупки товара."""
        self._print_header("Покупка товара")
        
        product_id = self._get_int_input("ID товара", min_val=1)
        if product_id is None:
            return
        
        try:
            product = self.app.find_by_id(product_id)
            self._print_product_details(product)
            
            if product.quantity == 0:
                self._print_error("Товар недоступен для покупки")
                return
            
            quantity = self._get_int_input("Количество для покупки", min_val=1, max_val=product.quantity)
            if quantity is None:
                return
            
            total = self.app.buy_product(product_id, quantity)
            
        except ItemNotFoundError as e:
            self._print_error(str(e))
        except ValueError as e:
            self._print_error(str(e))
    
    def menu_discount(self) -> None:
        """Меню управления скидками."""
        self._print_header("Управление скидками")
        
        print("1. Применить скидку к товару")
        print("2. Обновить скидки продуктов питания")
        print("3. Обновить скидки цифровых товаров")
        
        choice = self._get_int_input("Ваш выбор", min_val=1, max_val=3)
        if choice is None:
            return
        
        if choice == 1:
            product_id = self._get_int_input("ID товара", min_val=1)
            if product_id is None:
                return
            
            percent = self._get_int_input("Процент скидки", min_val=1, max_val=99)
            if percent is None:
                return
            
            try:
                self.app.apply_discount_to_product(product_id, percent)
                self._print_success(f"Скидка {percent}% применена")
            except (ItemNotFoundError, InvalidDataError) as e:
                self._print_error(str(e))
        
        elif choice == 2:
            self.app.update_food_products()
            self._print_success("Скидки продуктов питания обновлены")
        
        elif choice == 3:
            self.app.update_digital_products()
            self._print_success("Скидки цифровых товаров обновлены")
    
    def menu_statistics(self) -> None:
        """Показывает статистику."""
        self._print_header("Статистика коллекции")
        
        stats = self.app.get_statistics()
        
        print(f"{Fore.CYAN}Всего товаров:{Style.RESET_ALL} {stats['total_products']}")
        print(f"{Fore.CYAN}Общая стоимость:{Style.RESET_ALL} {stats['total_value']} руб.")
        print(f"{Fore.CYAN}Сэкономлено по скидкам:{Style.RESET_ALL} {stats['total_discount_saved']} руб.")
        print(f"{Fore.CYAN}Средняя цена:{Style.RESET_ALL} {stats['avg_cost']:.2f} руб.")
        print(f"{Fore.CYAN}Товаров со скидкой:{Style.RESET_ALL} {stats['products_with_discount']}")
        print()
    
    def menu_product_details(self) -> None:
        """Показывает детальную информацию о товаре."""
        self._print_header("Детальная информация")
        
        product_id = self._get_int_input("ID товара", min_val=1)
        if product_id is None:
            return
        
        try:
            product = self.app.find_by_id(product_id)
            self._print_product_details(product)
            
            print(f"\n{Fore.CYAN}--- История скидок ---{Style.RESET_ALL}")
            product.print_history()
            print()
            
        except ItemNotFoundError as e:
            self._print_error(str(e))
    
    def run(self) -> None:
        """Запускает главный цикл CLI."""
        self._print_info(f"Загружено товаров: {self.app.get_product_count()}")
        
        while self.running:
            self._print_menu()
            
            choice = self._get_int_input("\nВыберите пункт меню", min_val=0, max_val=14)
            if choice is None:
                continue
            
            self._execute_menu_item(choice)
    
    def _print_menu(self) -> None:
        """Печатает главное меню."""
        print(f"\n{Fore.CYAN}{'─' * 50}")
        print(f"{Style.BRIGHT}ГЛАВНОЕ МЕНЮ{Style.RESET_ALL}".center(50))
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        
        menu_items = [
            ("Показать все товары", 1),
            ("Показать доступные", 2),
            ("Показать со скидкой", 3),
            ("Поиск товаров", 4),
            ("Фильтрация", 5),
            ("Сортировка", 6),
            ("Добавить товар", 7),
            ("Купить товар", 8),
            ("Управление скидками", 9),
            ("Статистика", 10),
            ("Детали товара", 11),
            ("Удалить товар", 12),
            ("Сохранить и выйти", 13),
            ("Выход без сохранения", 0)
        ]
        
        for name, num in menu_items:
            print(f"  {num}. {name}")
        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
    
    def _execute_menu_item(self, choice: int) -> None:
        """
        Выполняет выбранный пункт меню.
        """
        menu_actions = {
            1: self.menu_show_all,
            2: self.menu_show_available,
            3: self.menu_show_with_discount,
            4: self.menu_search,
            5: self.menu_filter,
            6: self.menu_sort,
            7: self.menu_add_product,
            8: self.menu_buy_product,
            9: self.menu_discount,
            10: self.menu_statistics,
            11: self.menu_product_details,
            12: self.menu_remove_product,
            13: self.menu_save_and_exit,
            0: self.menu_exit
        }
        
        if choice in menu_actions:
            menu_actions[choice]()
        else:
            self._print_error("Неверный пункт меню")
    
    def menu_save_and_exit(self) -> None:
        """Сохраняет данные и выходит."""
        self._print_info("Сохранение данных...")
        self.running = False
    
    def menu_exit(self) -> None:
        """Выход без сохранения."""
        confirm = input(f"{Fore.YELLOW}Выйти без сохранения? (y/n): {Style.RESET_ALL}").lower()
        if confirm == 'y':
            self._print_info("Выход без сохранения")
            self.running = False
        else:
            self._print_info("Возврат в меню")