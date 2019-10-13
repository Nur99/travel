from copy import deepcopy
from functools import wraps
from rest_framework.status import is_success


def response_wrapper():
    """
    Decorator to make a view only accept request with required http method.
    :param required http method.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            if is_success(response.status_code):
                data = deepcopy(response.data)
                response.data = {'result': data, 'code': 0}
            return response
        return inner
    return decorator

