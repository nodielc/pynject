import pynject
import typing

from tests.sample_concrete_types import Weapon, Sword

container = pynject.PynjectContainer()

a_sword = Sword()

container.bind(Weapon).to_constant(a_sword)


@container.inject
def constants_binding_one(weapon: typing.Annotated[Weapon, pynject.Inject]) -> Weapon:
    return weapon


@container.inject
def constants_binding_two(weapon: typing.Annotated[Weapon, pynject.Inject]) -> Weapon:
    return weapon


def test_resolves_with_constant_variable() -> None:
    assert constants_binding_one() == constants_binding_two() == a_sword
