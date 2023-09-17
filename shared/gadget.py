from dataclasses import dataclass


@dataclass
class Gadget:
    name: str
    address: str

    def __str__(self):
        return f"{self.name} – {self.address}"
