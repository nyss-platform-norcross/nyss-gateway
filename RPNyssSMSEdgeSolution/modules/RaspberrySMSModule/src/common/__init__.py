import functools


class MemberDecoratorClass:

    def __init__(self, registry, func):
        self._registry = registry
        self._func = func

    def __call__(self, *args, **kwargs):
        self._func(*args, **kwargs)


class Component(type):
    def __init__(self, name, bases, attrs):
        oldInit = self.__init__

        def customInit(self, *args, **kwargs):
            for name, method in attrs.items():
                if isinstance(method, MemberDecoratorClass):
                    method._registry.append(
                        functools.partial(method._func, self))
            oldInit(self, *args, **kwargs)
        self.__init__ = customInit
