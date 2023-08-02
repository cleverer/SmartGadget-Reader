import gatt


class AnyDeviceManager(gatt.DeviceManager):
    def device_discovered(self, device):
        super().device_discovered(device)
        print("Discovered [%s] %s" % (device.mac_address, device.alias()))
