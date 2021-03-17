from pathlib import Path
from typing import List, Tuple, Dict
from pprint import pprint
from datetime import datetime, timedelta

import aiofiles
from fastapi import Form, UploadFile, File, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import Table

from dataSturct import Time
from database_op.sqlite3_op import table_get_inList_for_course_stu, get_session, build_table_in_DB, creat_course_table
from func_set.time_check import generate_deadline, check_time_outline, generate_fileTitle_time, get_last_time
from response import stu_form_reponses
from . import routers_

deadline: datetime = ...
File_Filter: Tuple[str, str] = ('.jpg', '.png')
table_cache: List[Table] = ...
current_alive_table: Table = ...
base_file_path: Path = Path(__file__).parent.parent / Path('data_file')
current_alive_file_path: Path = ...
stu_data: Dict = ...


@routers_.on_event("startup")
async def database_connect():
    global table_cache
    global stu_data
    table_cache, stu_table = table_get_inList_for_course_stu()
    session = next(get_session())
    pprint(table_cache)
    stu_data = dict(session.query(stu_table).all())
    pprint(stu_data)


@routers_.get('/get_time', tags=['学生'])
async def get_time():
    sec = get_last_time(deadline) if isinstance(deadline, datetime) else timedelta()
    return {"second": sec}


@routers_.post('/stu_msg_upload', tags=['学生'],
               responses={**stu_form_reponses})
# @check_time_decorator(deadline=deadline)
async def get_stu_data(  # request: requests.Request,
        stu_name: str = Form(...,
                             regex=r'^[^\x00-\xff]+$',
                             description='学生姓名'),
        stu_id: str = Form(...,
                           regex=r'^\d{10}$',
                           description='学生学号'),
        pic: UploadFile = File(..., description='注意！是图片类型'),
        session: Session = Depends(get_session)):
    """
    发送学生的学号姓名表单, 且上传的文件是图片类型！！！

    - **stu_name**: 学生的姓名
    - **pic**: 图片文件
    """
    # print(request.headers)
    # if check_time(deadline):
    #     raise HTTPException(status_code=403, detail="拒绝访问")
    # print(Path(pic.filename).suffix.lower())
    if check_time_outline(deadline):
        raise HTTPException(status_code=404, detail="超时！拒绝访问")
    if stu_id not in stu_data:
        raise HTTPException(status_code=401, detail="学号不存在！")
    if not stu_data.get(stu_id, default='') == stu_name:
        raise HTTPException(status_code=402, detail="学生姓名错误！")
    if Path(pic.filename).suffix.lower() not in File_Filter:
        raise HTTPException(status_code=403, detail="非图片类型")
    async with aiofiles.open(f'{str(current_alive_file_path)}/{stu_name}.jpg',
                             'wb') as f:
        await f.write(await pic.read())
    session.execute(
        current_alive_table.insert(), {
            'name': stu_name, 'pic_url': f'http://127.0.0.1:8000/static/{current_alive_file_path.name}/{stu_name}.jpg'})
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
        current_alive_file_path = base_file_path / \
            Path(f'{generate_fileTitle_time()}-{course}')
        current_alive_file_path.mkdir()
    return {'statue': 200}


@routers_.post('/stop_signIn', tags=["教师"])
async def stop_routine():
    """
    签到停止接口
    """
    global deadline
    deadline = generate_deadline()  # 默认为现在
    # print(deadline)
    # for table in table_cache:
    #     if table_name == table.name:
    #         return session.query(table).all()

    return {'status': 203}


@routers_.post('/face', tags=["学生"])
async def face_recognize():
    return '200'


@routers_.get('/excel_get', tags=["教师"])
async def creat_excel():
    return '200'
