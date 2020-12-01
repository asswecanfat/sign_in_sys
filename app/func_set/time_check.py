from functools import wraps
from fastapi import HTTPException
import asyncio
import datetime


# 谨慎使用！！！！
def check_time_decorator(deadline: datetime.datetime):
    """
    检查时间的修饰器，使用bug未知，谨慎使用

    >>> @check_time_decorator(deadline)
    >>> def func():
    >>>     pass
    :param deadline: datetime.datetime
    :return: inner_func
    """
    def innner_func(async_func):
        @wraps(async_func)
        def wraper(*args, **kwargs):
            if datetime.datetime.now() >= \
                    (deadline if isinstance(deadline, datetime.datetime) else datetime.datetime.now()):
                return asyncio.run(async_func(*args, **kwargs))
            raise HTTPException(status_code=403, detail="超时！拒绝访问")

        return wraper

    return innner_func


def check_time(deadline: datetime.datetime) -> bool:
    """
    检查当前时间是否过期

    :param deadline: datetime.datetime
    :return: bool
    """
    return datetime.datetime.now() >= deadline if isinstance(deadline, datetime.datetime) else datetime.datetime.now()


# 生成检验时间
def generate_deadline(**kwargs) -> datetime.datetime:
    """
    生成终止时间

    :param kwargs: seconds = float, minutes = float, hours = float)
    :return: datetime.datetime
    """

    def fliter(key: str) -> float:
        if value := kwargs.get(key):
            return value
        return 0

    return datetime.datetime.now() + datetime.timedelta(seconds=fliter('seconds'),
                                                        minutes=fliter('minutes'),
                                                        hours=fliter('hours'))

# if __name__ == '__main__':
#     @check_time(datetime.datetime.now())
#     def test(a, b):
#         return a+b
#
#     print(test(1, 2))
#     print(test.__name__)
