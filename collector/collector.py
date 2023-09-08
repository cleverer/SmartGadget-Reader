import logging

from shared import Data


class Collector:
    logger = logging.getLogger(__name__)

    @classmethod
    async def received(cls, data: Data) -> None:
        cls.logger.info(data)
