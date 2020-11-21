from datetime import datetime


# 服务器时间检测是否超时
async def sys_time_check(defalut_time: float) -> bool:
    return defalut_time >= datetime.now().timestamp()
