from smartgadget import NotifiableSmartGadget


def test_callback_temp(temp) -> None:
    print(f"Measured Temp: {temp}")


def test_callback_humid(temp) -> None:
    print(f"Measured humidity: {temp}")


def run():
    bedroom = NotifiableSmartGadget("FC:CE:02:A5:24:A7")
    # print(bedroom.get_values())

    bedroom.run(test_callback_temp, test_callback_humid)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    run()
