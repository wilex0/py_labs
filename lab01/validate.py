from datetime import datetime
from enums import *

def validate_strs(name: str):
        if not isinstance(name, str) or not len(name):
            raise TypeError("Incorrect name type")
        if not len(name):
            raise TypeError("Incorrect name length")
def validate_vals(v: int):
        if not isinstance(v, int):
            raise TypeError("Incorrect value type")
        if v <= 0:
            raise ValueError("Incorrect value")
def validate_size(size: Size):
        if not isinstance(size, Size):
            raise TypeError("Incorrect size type")
def validate_percent(perc: int):
        if not isinstance(perc, int):
            raise TypeError("Incorrect percent type")
        if not (0 < perc < 100):
              raise ValueError("Incorrect percent value")
def validate_date(date: datetime):
        if not isinstance(date, datetime):
            raise TypeError("Incorrect date type")