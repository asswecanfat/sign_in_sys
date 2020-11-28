import datetime


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
