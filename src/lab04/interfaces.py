from abc import ABC, abstractmethod
from typing import Any, List


class Updatable(ABC):
    @abstractmethod
    def update(self):
        pass
class Printable(ABC):
    @abstractmethod
    def print_history(self):
        pass
    @abstractmethod
    def to_string(self) -> str:
        pass
class Comparable(ABC):
    @abstractmethod 
    def compare_to(self, other) -> int:
        """
            -1 если текущий меньше other
            0 если равны
            1 если текущий больше other
        """
        pass
