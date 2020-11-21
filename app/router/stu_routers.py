from . import routers_
from fastapi import Form, UploadFile, File, HTTPException
from func_set.time_check import sys_time_check
from response import stu_form_reponses
from database_op.sqlite3_op import database, metadata, creat_table, engine
from pathlib import Path
import aiofiles


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


@routers_.post('/stuMsg_picUpload', tags=['上传表单'],
               responses={**stu_form_reponses})
async def get_stu_data(stu_name: str = Form(...,
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
    if _ := await sys_time_check(defalut_time=20):
        raise HTTPException(status_code=403, detail="拒绝访问")

    context = await pic.read()
    file_path = Path(__file__).parent.parent / Path('data_file')
    async with aiofiles.open(f'{str(file_path)}/{pic.filename}', 'wb') as f:
        await f.write(context)
    return {"stu_name": stu_name,
            "stu_id": stu_id}


@routers_.post('start_signIn')
async def start(token: str = Form(...)):
    """
    管理员开启签到接口
    - **token**: 验证码
    """
    ...

