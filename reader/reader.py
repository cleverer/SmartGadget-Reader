import logging

from sensirionbt import SmartGadget

from collector import Collector
from shared import Data


class Reader:
    logger = logging.getLogger(__name__)

    @classmethod
    def process_gadget(cls, gadget_address: str):
        cls.logger.info(f"Processing Gadget {gadget_address}")
        bedroom = SmartGadget(gadget_address)
        data = Data(**bedroom.get_values())
        cls.logger.debug(f"Received {data}")
        Collector.received(data)

    @classmethod
    def read(cls):
        cls.logger.info("Reading…")
        for gadget in ["FC:CE:02:A5:24:A7"]:
            cls.process_gadget(gadget)
