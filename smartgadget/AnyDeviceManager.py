import gatt


class AnyDeviceManager(gatt.DeviceManager):
    @staticmethod
    def device_discovered(device):
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))
