from functools import wraps


class Decorators:
    @staticmethod
    def singleton(class_: object) -> object:
        instances = {}

        def getinstance(*args, **kwargs):
            if class_ not in instances:
                instances[class_] = class_(*args, **kwargs)
            return instances[class_]

        return getinstance
