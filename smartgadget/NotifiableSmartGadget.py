from typing import Any, Callable

from sensirionbt import SmartGadget
from sensirionbt.constants import (
    SHT3X_HUMIDITY_NOTIFICATIONS_UUID,
    SHT3X_TEMPERATURE_NOTIFICATIONS_UUID,
)

from .NotifiableBTLEConnection import NotifiableBTLEConnection


def _register_temp_callback(c, callback: Callable[[Any], None]):
    handle = c.subscribe_characteristic(SHT3X_TEMPERATURE_NOTIFICATIONS_UUID)
    c.set_callback(handle, callback)


def _register_humidity_callback(c, callback: Callable[[Any], None]):
    handle = c.subscribe_characteristic(SHT3X_HUMIDITY_NOTIFICATIONS_UUID)
    c.set_callback(handle, callback)


def _deregister_temp_callback(c):
    handle = c.unsubscribe_characteristic(SHT3X_TEMPERATURE_NOTIFICATIONS_UUID)
    c.remove_callback(handle)


def _deregister_humidity_callback(c):
    handle = c.unsubscribe_characteristic(SHT3X_HUMIDITY_NOTIFICATIONS_UUID)
    c.remove_callback(handle)


class NotifiableSmartGadget(SmartGadget):
    def __init__(self, mac, connection_cls=NotifiableBTLEConnection):
        super().__init__(mac, connection_cls)

    def run(
        self,
        temp_callback: Callable[[Any], None],
        humid_callback: Callable[[Any], None],
    ):
        with self._conn as c:
            _register_temp_callback(c, temp_callback)
            _register_humidity_callback(c, humid_callback)

            try:
                c.wait_for_notifications()
            except KeyboardInterrupt:
                pass
            except Exception:
                pass

            _deregister_temp_callback(c)
            _deregister_humidity_callback(c)
