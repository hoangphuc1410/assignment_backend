import time
from functools import wraps

from fastapi import Request, HTTPException


def rate_limited(max_calls: int, time_frame: int):
    """
    :param max_calls: The maximum number of calls allowed within the time frame.
    :param time_frame: The time frame in seconds during which the calls are counted.
    """
    def decorator(func):
        calls = 0
        last_reset = 0

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            nonlocal calls, last_reset
            current_time = time.time()

            if current_time - last_reset > time_frame:
                calls = 0
                last_reset = current_time

            if calls < max_calls:
                calls += 1
                return await func(request, *args, **kwargs)
            else:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

        return wrapper

    return decorator
