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
