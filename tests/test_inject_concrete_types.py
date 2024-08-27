import typing

from tests.sample_concrete_types import Weapon, Sword, M1911
import pynject


bind_without_args_container = pynject.PynjectContainer()
bind_without_args_container.bind(Weapon).to(Sword)

bind_with_args_container = pynject.PynjectContainer()
bind_with_args_container.bind(Weapon).to(M1911, ammo_type=".45 ACP")


@bind_without_args_container.inject
def no_args_bind_attack(weapon: typing.Annotated[Weapon, pynject.Inject]) -> str:
    return weapon.attack()


@bind_with_args_container.inject
def bind_with_args_attack(weapon: typing.Annotated[Weapon, pynject.Inject]) -> str:
    return weapon.attack()


def test_resolves_correct_weapon_without_args() -> None:
    assert no_args_bind_attack() == "Attacking with Generic sword"


def test_resolves_correct_weapon_with_args() -> None:
    assert bind_with_args_attack() == "M1911 shoots .45 ACP"
