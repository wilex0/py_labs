from enum import Enum

class Size(Enum):
    SMALL = 1
    NORMAL = 2
    BIG = 3
    def __str__(self):
        match(self):
            case Size.SMALL:
                return "Small"
            case Size.NORMAL:
                return "Normal"
            case Size.BIG:
                return "Big"