import asyncio
import datetime
import logging
from typing import Iterable, Optional

from sensirionbt import SmartGadget

from collector import Collector
from shared import Measurement
from shared.gadget import Gadget


class Reader:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._collector: Optional[Collector] = None

    @property
    def collector(self) -> Collector:
        if self._collector is None:
            self._collector = Collector()
        return self._collector

    async def process_gadget(self, gadget: Gadget) -> Optional[Measurement]:
        try:
            self.logger.info(f"Processing Gadget {gadget}")
            bedroom = SmartGadget(gadget.address)
            values = bedroom.get_values()
            now = datetime.datetime.utcnow()
            data = Measurement(time=now, sensor=gadget, **values)
            self.logger.debug(f"Received {data}")
            return data
        except Exception as e:
            self.logger.error(f"Processing Gadget {gadget} failed", exc_info=e)
            return None

    async def read(self) -> None:
        self.logger.info("Reading…")
        gadgets = [
            Gadget(name="Schlafzimmer", address=""),
            Gadget(name="Balkon", address=""),
        ]
        tasks = [self.process_gadget(gadget) for gadget in gadgets]
        data: Iterable[Optional[Measurement]] = await asyncio.gather(*tasks)
        filtered_data: Iterable[Measurement] = filter(
            lambda measurement: measurement is not None, data
        )
        await self.collector.received(filtered_data)

    async def close(self) -> None:
        await self.collector.close()
