class ItemNotFoundError(Exception):
    """Объект не найден в коллекции."""
    def __init__(self, message: str = "Товар не найден"):
        self.message = message
        super().__init__(self.message)


class DuplicateItemError(Exception):
    """Объект с таким идентификатором уже существует."""
    def __init__(self, message: str = "Товар с таким ID уже существует"):
        self.message = message
        super().__init__(self.message)


class InvalidDataError(Exception):
    """Некорректные данные для создания/обновления товара."""
    def __init__(self, message: str = "Некорректные данные"):
        self.message = message
        super().__init__(self.message)


class StorageError(Exception):
    """Ошибка при сохранении/загрузке данных."""
    def __init__(self, message: str = "Ошибка работы с файлом"):
        self.message = message
        super().__init__(self.message)