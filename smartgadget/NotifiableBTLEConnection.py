from sensirionbt.connection import BTLEConnection


class NotifiableBTLEConnection(BTLEConnection):
    def __init__(self, mac, retries=2):
        super().__init__(mac, retries)

    def wait_for_notifications(self):
        self._conn.waitForNotifications(timeout=None)
