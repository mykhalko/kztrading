__all__ = ['logging']

import functools
import types

class ParameterTransmission:
    def __init__(self, decorator):
        self.decorator = decorator

    def __call__(self, *args, **kwargs):
        decorator = self.decorator

        @functools.wraps(decorator)
        def decorator_wrapper(f):
            return decorator(f, *args, **kwargs)
        return decorator_wrapper


@ParameterTransmission
def logging(executable, start_msg=None, end_msg=None):
    if start_msg is None:
        start_msg = executable.__name__ + ' started'
    if end_msg is None:
        end_msg = executable.__name__ + ' finished'

    @functools.wraps(executable)
    def wrapper(*args, **kwargs):
        print(start_msg)
        result = executable(*args, **kwargs)
        print(end_msg)
        return result
    return wrapper


def class_logging(cls):
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if isinstance(attr, types.FunctionType):
            setattr(cls, attr_name,
                    logging(start_msg='# ' + cls.__name__ + ':' + attr_name + ' started',
                            end_msg='# ' + cls.__name__ + ':' + attr_name + ' finished')
                    (attr))
    return cls
