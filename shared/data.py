from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Data:
    temperature: Decimal
    humidity: Decimal
    battery_level: int
