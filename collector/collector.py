from shared import Data


class Collector:
    @classmethod
    def received(cls, data: Data) -> None:
        print(data)
