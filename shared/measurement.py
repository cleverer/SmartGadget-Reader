# Copyright (C) 2023 Nicolas Da Mutten
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
