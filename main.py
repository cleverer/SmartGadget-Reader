from smartgadget import SHT40, AnyDeviceManager


def test_callback_temp(temp: int) -> None:
    print(f"Measured Temp: {temp}")


def test_callback_humid(temp: int) -> None:
    print(f"Measured humidity: {temp}")


def run():
    manager = AnyDeviceManager(adapter_name="hci0")
    manager.start_discovery(service_uuids=[SHT40.t_uuid, SHT40.h_uuid])
    print("Started Discovery")

    bedroom = SHT40(
        mac_address="",
        manager=manager,
        temperature_callback=test_callback_temp,
        humidity_callback=test_callback_humid,
    )

    bedroom.connect()

    print("bedroom connected. Stopping discovery")

    # all devices connected, so stop discovering
    manager.stop_discovery()

    print("Discovery Stopped. Starting run loop")

    # RunLoop
    try:
        manager.run()
    except KeyboardInterrupt:
        pass
    finally:
        if callable(bedroom.disconnect):
            print("disconnecting")
            bedroom.disconnect()
            print("disconnected")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    run()
