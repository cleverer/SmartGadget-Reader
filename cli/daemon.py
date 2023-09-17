import asyncio
import logging
from os import environ

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger

from reader import Reader


class Daemon:
    logger = logging.getLogger(__name__)

    def __init__(self, reader: Reader):
        self.reader = reader

    def prepare_scheduler(self, cron: str) -> BaseScheduler:
        self.logger.debug("Using AsyncIOScheduler")
        scheduler = AsyncIOScheduler()
        self.logger.debug(f"Scheduling Data Collection: {cron}")
        schedule = CronTrigger.from_crontab(cron)

        scheduler.add_job(self.reader.read, schedule)

        scheduler.start()

        return scheduler

    def main(self) -> None:
        # Create an asyncio event loop
        loop = asyncio.get_event_loop()

        cron = environ.get("SCHEDULE", "*/10 * * * *")
        scheduler = self.prepare_scheduler(cron)

        self.logger.info("Starting daemon")
        try:
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            scheduler.shutdown()
            loop.run_until_complete(self.reader.close())
            self.logger.info("Stopping daemon")
