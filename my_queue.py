from typing import TypeVar, Generic

T = TypeVar('T')


class Queue(Generic[T]):
    _list: list[T]

    def __init__(self, init: list[T] = None):
        self._list = list(init) or list()

    def __repr__(self) -> T:
        return repr(self._list)

    def push(self, item: T):
        self._list.append(item)

    def pop(self) -> T:
        x = self._list[0]
        self._list = self._list[1:]
        return x

    def peek(self) -> T:
        return self._list[0]