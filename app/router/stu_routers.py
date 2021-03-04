from pathlib import Path
from typing import List, Tuple
from sqlalchemy import Table
from datetime import datetime

import aiofiles
from fastapi import Form, UploadFile, File, requests, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError

from dataSturct import Time
from database_op.sqlite3_op import table_get_inList, get_session, build_table_in_DB, creat_course_table
from func_set.time_check import generate_deadline, check_time_decorator, generate_fileTitle_time
from response import stu_form_reponses
from . import routers_
from pprint import pprint

deadline: datetime = ...
File_Filter: Tuple[str, str] = ('.jpg', '.png')
table_cache: List[Table] = ...
current_alive_table: Table = ...
base_file_path: Path = Path(__file__).parent.parent / Path('data_file')
current_alive_file_path: Path = ...


@routers_.on_event("startup")
async def database_connect():
    global table_cache
    table_cache = table_get_inList()
    pprint(table_cache)


@routers_.post('/stu_msg_upload', tags=['学生'],
               responses={**stu_form_reponses})
@check_time_decorator(deadline=deadline)
async def get_stu_data(  # request: requests.Request,
        stu_name: str = Form(...,
                             regex=r'^[^\x00-\xff]+$',
                             description='学生姓名'),
        # stu_id: str = Form(...,
        #                    regex=r'^\d{10}$',
        #                    description='学生学号'),
        pic: UploadFile = File(..., description='注意！是图片类型'),
        session: Session = Depends(get_session)):
    """
    发送学生的学号姓名表单, 且上传的文件是图片类型！！！

    - **stu_name**: 学生的姓名表单
    - **stu_id**: 学生的学号表单
    - **pic**: 图片文件
    """
    # print(request.headers)
    # if check_time(deadline):
    #     raise HTTPException(status_code=403, detail="拒绝访问")
    print(Path(pic.filename).suffix.lower())
    if Path(pic.filename).suffix.lower() not in File_Filter:
        raise HTTPException(status_code=403, detail="非图片类型")
    async with aiofiles.open(f'{str(current_alive_file_path)}/{stu_name}.jpg',
                             'wb') as f:
        await f.write(await pic.read())
    session.execute(current_alive_table.insert(), {'name': stu_name,
                                                   'pic_url': 'test_url'})
    session.commit()
    return {"status": 200}


@routers_.post('/start_signIn', tags=["教师"])
async def start(time: Time,
                course: str = Body(...,
                                   description="课程名")):
    """
    管理员开启签到接口
    - **seconds**: 持续秒数
    - **minutes**: 持续分钟数
    - **hours**: 持续小时数
    """
    global deadline
    global current_alive_table
    global current_alive_file_path
    try:
        current_alive_table = creat_course_table(course)
    except InvalidRequestError:
        raise HTTPException(status_code=403, detail=f"该表-{course}-已创建！")
    else:
        deadline = generate_deadline(seconds=time.seconds,
                                     minutes=time.minutes,
                                     hours=time.hours)
        build_table_in_DB(current_alive_table)
        current_alive_file_path = base_file_path / Path(f'{generate_fileTitle_time()}-{course}')
        current_alive_file_path.mkdir()
    return {'statue': 200}


@routers_.post('/stop_signIn', tags=["教师"])
async def stop_routine():
    global deadline
    deadline = generate_deadline()  # 默认为现在
    # print(deadline)
    # for table in table_cache:
    #     if table_name == table.name:
    #         return session.query(table).all()

    return {'status': 203}
