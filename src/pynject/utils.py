import typing

TFirstItem = typing.TypeVar("TFirstItem")


def first(collection: typing.Collection[TFirstItem]) -> typing.Optional[TFirstItem]:
    try:
        return next(iter(collection))
    except StopIteration:
        return None
