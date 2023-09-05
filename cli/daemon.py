import logging
import signal
from os import environ

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.cron import CronTrigger

from reader import Reader


class Daemon:
    logger = logging.getLogger(__name__)

    @classmethod
    def prepare_scheduler(cls, cron: str) -> BaseScheduler:
        cls.logger.debug("Using BlockingScheduler")
        scheduler = BlockingScheduler()
        cls.logger.debug(f"Scheduling Data Collection: {cron}")
        schedule = CronTrigger.from_crontab(cron)

        scheduler.add_job(Reader.read, schedule)

        # In order to shut down clean, capture system signals
        # and shut down the scheduler.
        def graceful_shutdown(signum, frame) -> None:
            scheduler.shutdown()

        signal.signal(signal.SIGINT, graceful_shutdown)
        signal.signal(signal.SIGTERM, graceful_shutdown)
        return scheduler

    @classmethod
    def run(cls) -> None:
        cron = environ.get("SCHEDULE", "*/1 * * * *")
        scheduler = Daemon.prepare_scheduler(cron)
        cls.logger.info("Starting daemon")
        scheduler.start()
        cls.logger.info("Stopping daemon")
