import struct
from typing import Any, Callable

import gatt


class SHT40(gatt.Device):
    t_uuid = "00002235-b38d-4985-720e-0f993a68ee41"
    h_uuid = "00001235-b38d-4985-720e-0f993a68ee41"

    def __init__(
        self,
        mac_address: str,
        manager: gatt.DeviceManager,
        temperature_callback: Callable[[int], None],
        humidity_callback: Callable[[int], None],
    ) -> None:
        super().__init__(mac_address=mac_address.lower(), manager=manager)
        self.temperature_callback = temperature_callback
        self.humidity_callback = humidity_callback

    def services_resolved(self) -> None:
        super().services_resolved()

        print("Resolved services")

        for s in self.services:
            if s.uuid == "00002234-b38d-4985-720e-0f993a68ee41":
                temperature_service = s
            elif s.uuid == "00001234-b38d-4985-720e-0f993a68ee41":
                humidity_service = s

        temperature_characteristic = next(
            c for c in temperature_service.characteristics if c.uuid == self.t_uuid
        )

        humidity_characteristic = next(
            c for c in humidity_service.characteristics if c.uuid == self.h_uuid
        )

        temperature_characteristic.enable_notifications()
        humidity_characteristic.enable_notifications()

    @staticmethod
    def characteristic_enable_notifications_succeeded(
        characteristic: gatt.Characteristic,
    ) -> None:
        print(f"Subscription to change notifications ({characteristic.uuid}) - SUCCESS")

    @staticmethod
    def characteristic_enable_notifications_failed(
        characteristic: gatt.Characteristic,
    ) -> None:
        print(f"Subscription to change notifications ({characteristic.uuid}) - FAIL!")

    def characteristic_value_updated(
        self, characteristic: gatt.Characteristic, value: Any
    ) -> None:
        value: int = round(struct.unpack("<f", value)[0], 1)
        if characteristic.uuid == self.t_uuid:
            if callable(self.temperature_callback):
                self.temperature_callback(value)
        elif characteristic.uuid == self.h_uuid:
            if callable(self.humidity_callback):
                self.humidity_callback(value)
