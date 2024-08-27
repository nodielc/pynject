import typing


class Weapon(typing.Protocol):
    def attack(self) -> str: ...


class Sword:
    def __init__(self, sword: str = "Generic sword") -> None:
        self.sword = sword

    def attack(self) -> str:
        return f"Attacking with {self.sword}"


class M1911:

    def __init__(self, ammo_type: str) -> None:
        self.ammo_type = ammo_type

    def attack(self) -> str:
        return f"M1911 shoots {self.ammo_type}"
