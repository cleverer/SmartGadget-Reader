import logging

from sensirionbt import SmartGadget


class Reader:
    logger = logging.getLogger(__name__)

    @classmethod
    def read(cls):
        bedroom = SmartGadget("FC:CE:02:A5:24:A7")
        print(bedroom.get_values())
