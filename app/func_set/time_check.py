# from functools import wraps
# from fastapi import HTTPException
# import asyncio
import datetime


# # 谨慎使用！！！！
# def check_time_decorator(deadline: datetime.datetime):
#     """
#     检查时间的修饰器，使用bug未知，谨慎使用
#
#     >>> @check_time_decorator(deadline)
#     >>> async def func():
#     >>>     pass
#     :param deadline: datetime.datetime
#     :return: inner_func
#     """
#
#     def innner_func(async_func):
#         @wraps(async_func)
#         def wraper(*args, **kwargs):
#             if datetime.datetime.now() < \
#                     (deadline if isinstance(deadline, datetime.datetime) else datetime.datetime.now()):
#                 return asyncio.run(async_func(*args, **kwargs))
#             print(deadline)
#             raise HTTPException(status_code=403, detail="超时！拒绝访问")
#
#         return wraper
#
#     return innner_func


def check_time_outline(deadline: datetime.datetime) -> bool:
    """
    检查当前时间是否过期（可用于fastapi的依赖）

    :param deadline: datetime.datetime
    :return: bool
    """
    return datetime.datetime.now() >= deadline if isinstance(deadline, datetime.datetime) else datetime.datetime.now()


# 生成检验时间
def generate_deadline(seconds: float = 0,
                      minutes: float = 0,
                      hours: float = 0) -> datetime.datetime:
    """
    生成终止时间

    :param hours:
    :param minutes:
    :param seconds:
    :return: datetime.datetime
    """
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds,
                                                        minutes=minutes,
                                                        hours=hours)


def generate_fileTitle_time() -> str:
    return f'{str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M"))}'


def get_last_time(deadline: datetime.datetime) -> datetime.timedelta:
    if (last_time := deadline - datetime.datetime.now()) < datetime.timedelta():
        last_time = datetime.timedelta()
    return last_time

# if __name__ == '__main__':
#     @check_time(datetime.datetime.now())
#     def test(a, b):
#         return a + b
#
#
#     print(test(1, 2))
#     print(test.__name__)
#     print(generate_fileTitle_time())
