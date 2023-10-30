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

import logging
import os
from typing import Iterable

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from shared import Measurement

token = os.environ.get("INFLUXDB_TOKEN")
org = "org"
url = "url"

bucket = "bucket2"


class Collector:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.client = InfluxDBClientAsync(url=url, token=token, org=org)
        self.write_api = self.client.write_api()

    async def received(self, data: Iterable[Measurement]) -> None:
        points = []
        for measurement in data:
            self.logger.info(f"Got {measurement}")
            points.extend(measurement.points())

        self.logger.info(f"Logging points: {points}")

        await self.write_api.write(bucket=bucket, record=points)

    async def close(self) -> None:
        await self.client.close()
