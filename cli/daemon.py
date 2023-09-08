import asyncio
import logging
from os import environ

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger

from reader import Reader


class Daemon:
    logger = logging.getLogger(__name__)

    @classmethod
    def prepare_scheduler(cls, cron: str) -> BaseScheduler:
        cls.logger.debug("Using AsyncIOScheduler")
        scheduler = AsyncIOScheduler()
        cls.logger.debug(f"Scheduling Data Collection: {cron}")
        schedule = CronTrigger.from_crontab(cron)

        scheduler.add_job(Reader.read, schedule)

        scheduler.start()

        return scheduler

    @classmethod
    def main(cls) -> None:
        # Create an asyncio event loop
        loop = asyncio.get_event_loop()

        cron = environ.get("SCHEDULE", "*/10 * * * *")
        scheduler = Daemon.prepare_scheduler(cron)

        cls.logger.info("Starting daemon")
        try:
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            scheduler.shutdown()
            cls.logger.info("Stopping daemon")
