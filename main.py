from sensirionbt import SmartGadget


def test_callback_temp(temp: int) -> None:
    print(f"Measured Temp: {temp}")


def test_callback_humid(temp: int) -> None:
    print(f"Measured humidity: {temp}")


def run():
    bedroom = SmartGadget("FC:CE:02:A5:24:A7")
    bedroom.set


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    run()
