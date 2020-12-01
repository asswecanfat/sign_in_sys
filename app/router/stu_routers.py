from . import routers_
from dataSturct import Time
from fastapi import Form, UploadFile, File, requests, HTTPException
from func_set.time_check import generate_deadline, check_time_decorator
from response import stu_form_reponses
from database_op.sqlite3_op import database, metadata, creat_table, engine
from pathlib import Path
import aiofiles

deadline = ...
FileFliter = ('jpg', 'JPG', 'png', 'PNG')


@routers_.on_event("startup")
async def database_connect():
    await database.connect()
    data_table = creat_table("test", metadata)
    metadata.create_all(engine, tables=[data_table], checkfirst=True)
    # await database.execute(test.insert().values(id='123', name='asd'))
    # print(await database.fetch_all(data_table.select()))


@routers_.on_event("shutdown")
async def database_realse():
    await database.disconnect()


@routers_.post('/stu_msg_upload', tags=['上传表单'],
               responses={**stu_form_reponses})
@check_time_decorator(deadline=deadline)
async def get_stu_data(request: requests.Request,
                       stu_name: str = Form(...,
                                            regex=r'^[^\x00-\xff]+$',
                                            description='学生姓名'),
                       stu_id: str = Form(...,
                                          regex=r'^\d{10}$',
                                          description='学生学号'),
                       pic: UploadFile = File(..., description='注意！是图片类型')):
    """
    发送学生的学号姓名表单, 且上传的文件是图片类型！！！

    - **stu_name**: 学生的姓名表单
    - **stu_id**: 学生的学号表单
    - **pic**: 图片文件
    """
    # print(request.client)
    # if check_time(deadline):
    #     raise HTTPException(status_code=403, detail="拒绝访问")
    if pic.filename.split('.')[-1] not in FileFliter:
        raise HTTPException(status_code=403, detail="非图片类型")
    file_path = Path(__file__).parent.parent / Path('data_file')
    async with aiofiles.open(f'{str(file_path)}/{pic.filename}', 'wb') as f:
        await f.write(await pic.read())
    return {"stu_name": stu_name,
            "stu_id": stu_id}


@routers_.post('/start_signIn', tags=["管理员api"])
async def start(time: Time):
    """
    管理员开启签到接口
    - **seconds**: 持续秒数
    - **minutes**: 持续分钟数
    - **hours**: 持续小时数
    """
    global deadline
    deadline = generate_deadline(seconds=time.seconds,
                                 minutes=time.minutes,
                                 hours=time.hours)
    return 200
