import typing
import inspect
import functools

from . import utils
from . import markers
from . import bindings


TReturn = typing.TypeVar("TReturn")


class PynjectContainer:
    _registry: dict[type, bindings.ConcreteWrapper]

    def __init__(self) -> None:
        self._registry = {}

    def __process_parameters_to_inject(
        self, parameters: typing.Mapping[str, inspect.Parameter]
    ) -> list[inspect.Parameter]:
        translated_parameters: list[inspect.Parameter] = []

        for param in parameters.values():
            if self.__is_param_annotated_to_inject(param):
                abstract_type = utils.first(typing.get_args(param.annotation))

                if abstract_type is None:
                    raise ValueError("No base type defined")

                if not self.__can_resolve_abstract(abstract_type):
                    raise ValueError(f"Cannot resolve type {abstract_type}")

                concrete_resolver = self._registry[abstract_type]
                injected_param = param.replace(default=concrete_resolver.resolve())
                translated_parameters.append(injected_param)

                continue

            translated_parameters.append(param)

        return translated_parameters

    def __is_param_annotated_to_inject(self, param: inspect.Parameter) -> bool:
        is_annotated = typing.get_origin(param.annotation) is typing.Annotated
        annotated_args = typing.get_args(param.annotation)

        return is_annotated and utils.first(annotated_args[1:]) is markers.Inject

    def __can_resolve_abstract(self, abstract_type: type) -> bool:
        return abstract_type in self._registry

    def bind(self, abstract_type: type) -> bindings.ConcreteBinding:
        return bindings.ConcreteBinding(abstract_type, self._registry)

    def inject(
        self, func: typing.Callable[..., TReturn]
    ) -> typing.Callable[..., TReturn]:
        original_signature = inspect.signature(func)
        translated_params = self.__process_parameters_to_inject(
            original_signature.parameters
        )

        injected_signature = original_signature.replace(parameters=translated_params)

        @functools.wraps(func)
        def _inject(*args: typing.Any, **kwargs: typing.Any) -> TReturn:
            bound_parameters = injected_signature.bind_partial(*args, **kwargs)
            bound_parameters.apply_defaults()

            return func(*bound_parameters.args, **bound_parameters.kwargs)

        return _inject
