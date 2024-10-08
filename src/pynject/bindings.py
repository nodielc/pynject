import typing


class ConcreteWrapper(typing.Protocol):

    def resolve(self) -> typing.Any:
        pass


class ConcretesFactoryWrapper:
    def __init__(
        self, concrete_type: type, *args: typing.Any, **kwargs: typing.Any
    ) -> None:
        self._concrete_type = concrete_type
        self._args = args
        self._kwargs = kwargs

    def resolve(self) -> typing.Any:
        return self._concrete_type(*self._args, **self._kwargs)


class ConstantsFactoryWrapper:
    def __init__(self, value: typing.Any) -> None:
        self.value = value

    def resolve(self) -> typing.Any:
        return self.value


class ConcreteBinding:

    def __init__(
        self,
        abstract_type: type,
        registry: dict[type, ConcreteWrapper],
    ):
        self._registry = registry
        self._abstract_type = abstract_type

    def to(self, concrete_type: type, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._registry[self._abstract_type] = ConcretesFactoryWrapper(
            concrete_type, *args, **kwargs
        )

    def to_constant(self, value: typing.Any) -> None:
        self._registry[self._abstract_type] = ConstantsFactoryWrapper(value=value)
