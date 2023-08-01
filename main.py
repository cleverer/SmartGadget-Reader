import gatt

from smartgadget import SHT40


def test_callback_temp(temp: int) -> None:
    print(f"Measured Temp: {temp}")


def test_callback_humid(temp: int) -> None:
    print(f"Measured Temp: {temp}")


def run():
    manager = gatt.DeviceManager(adapter_name="hci0")
    bedroom = SHT40(
        mac_address="",
        manager=manager,
        temperature_callback=test_callback_temp,
        humidity_callback=test_callback_humid,
    )

    bedroom.connect()

    # RunLoop
    manager.run()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    run()
