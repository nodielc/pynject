# Pynject

## Overview

Pynject is a simple and lightweight Dependency Injection (DI) framework for Python. It helps you manage your code dependencies more cleanly, making your applications more modular, testable, and easier to maintain.

## Features

- **Easy to Use**: Set up DI in just a few steps.
- **Lightweight**: No heavy dependencies, just pure Python.

## Installation

NOT YET


## Usage


### Factory dependency injection

```python
import typing
from pynject import PynjectContainer, Inject


class Weapon(typing.Protocol):

    def attack(self) -> str:
        pass


class Sword:
    def __init__(self, sword_type: str = "Katana") -> None:
        self.sword_type = sword_type

    def attack(self) -> str:
        return f"attacking with a {self.sword_type}"


container = PynjectContainer()

container.bind(Weapon).to(Sword)


@container.inject
def main(weapon: typing.Annotated[Weapon, Inject]) -> None:
    print(weapon.attack())


main()
```
---
```sh
>>> "attacking with a Katana"
```

Parameters can also be passed to construct a concrete type

```python
# ...

container.bind(Weapon).to(Sword, sword_type="Scimitar")

@container.inject
def main(weapon: typing.Annotated[Weapon, Inject]) -> None:
    print(weapon.attack())

main()
```
---
```sh
>>> "attacking with a Scimitar"
```

### Singleton dependency injection


```python
import typing
from pynject import PynjectContainer, Inject


class Weapon(typing.Protocol):

    def attack(self) -> str:
        pass


class Sword:
    def __init__(self, sword_type: str = "Katana") -> None:
        self.sword_type = sword_type

    def attack(self) -> str:
        return f"attacking with a {self.sword_type}"


long_sword = Sword(sword_type="Long sword")


container = PynjectContainer()
container.bind(Weapon).to_constant(long_sword)


@container.inject
def service_a(weapon: typing.Annotated[Weapon, Inject]) -> Weapon:
    return weapon


@container.inject
def service_b(weapon: typing.Annotated[Weapon, Inject]) -> Weapon:
    return weapon


print(service_a() == service_b() == long_sword)
```
---
```sh
>>> True
```
