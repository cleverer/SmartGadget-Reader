from smartgadget import SHT40, AnyDeviceManager


def test_callback_temp(temp: int) -> None:
    print(f"Measured Temp: {temp}")


def test_callback_humid(temp: int) -> None:
    print(f"Measured humidity: {temp}")


def run():
    manager = AnyDeviceManager(adapter_name="hci0")
    manager.start_discovery()

    bedroom = SHT40(
        mac_address="",
        manager=manager,
        temperature_callback=test_callback_temp,
        humidity_callback=test_callback_humid,
    )

    bedroom.connect()

    # RunLoop
    try:
        manager.run()
    except Exception:
        pass

    if callable(bedroom.disconnect):
        bedroom.disconnect()
        print("disconnected")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    run()
