import asyncio
import logging

from sensirionbt import SmartGadget

from collector import Collector
from shared import Data


class Reader:
    logger = logging.getLogger(__name__)

    @classmethod
    async def process_gadget(cls, gadget_address: str):
        cls.logger.info(f"Processing Gadget {gadget_address}")
        bedroom = SmartGadget(gadget_address)
        data = Data(**bedroom.get_values())
        cls.logger.debug(f"Received {data}")
        await Collector.received(data)

    @classmethod
    async def read(cls):
        cls.logger.info("Reading…")
        gadgets = ["FC:CE:02:A5:24:A7", "EA:66:DF:61:46:D1"]
        tasks = [cls.process_gadget(gadget) for gadget in gadgets]
        await asyncio.gather(*tasks)
