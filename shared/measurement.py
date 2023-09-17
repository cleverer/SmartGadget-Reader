from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from influxdb_client import Point

from shared.gadget import Gadget


@dataclass
class Measurement:
    temperature: Decimal
    humidity: Decimal
    battery_level: int
    time: datetime
    sensor: Gadget

    def temperature_point(self):
        return (
            Point("temperature")
            .tag("sensor", self.sensor.name)
            .field("actual", self.temperature)
            .time(self.time)
        )

    def humidity_point(self):
        return (
            Point("humidity")
            .tag("sensor", self.sensor.name)
            .field("actual", self.humidity)
            .time(self.time)
        )

    def battery_level_point(self):
        return (
            Point("battery_level")
            .tag("sensor", self.sensor.name)
            .field("actual", self.battery_level)
            .time(self.time)
        )

    def points(self) -> list[Point]:
        return [
            self.temperature_point(),
            self.humidity_point(),
            self.battery_level_point(),
        ]
